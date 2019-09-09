#!/bin/bash
# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FS_LIMIT=80
DOCS_DROP=100000
ES_URL="http://localhost:$ELASTICSEARCH_LOGGING_SERVICE_PORT"

log () {
    echo "LOGROTATE: $*" >/proc/1/fd/1
}

log "hourly job started"

IFS='-' read es type num <<< "$HOSTNAME"
if [[ "$type" != "data" ]]; then
    log "non-data node -> exiting"
    exit 0
fi

# sleep to avoid concurrent runs across multiple ES data Pods
let "SLEEP=($num * 600)+($RANDOM % 30)"
log "sleeping $SLEEP seconds..."
sleep $SLEEP

TODAY=`date -u +%Y.%m.%d`
declare -i pcent=100
while [ $pcent -ge $FS_LIMIT ]
do
    pcent=`df --output=pcent /usr/share/elasticsearch/data | tail -n1 | tr -d '%'`
    log "current filesystem usage: $pcent%"
    if [ $pcent -le $FS_LIMIT ]; then break; fi
    index_drop=`curl -sS -XGET "$ES_URL/_cat/indices?h=index" | egrep '^.+-[[:digit:]]{4}\.[[:digit:]]{2}\.[[:digit:]]{2}$' | grep -v "$TODAY" | sort -t'-' -k2 | head -n1`
    if [ -n "$index_drop" ]; then
        log "drop index: $index_drop"
        curl -sS -XDELETE "$ES_URL/$index_drop" >/dev/null
        sleep 5
    else
        log "drop oldest $DOCS_DROP log entries"
        curl -sS -XPOST "$ES_URL/*-$TODAY/_delete_by_query?sort=@timestamp:asc&max_docs=$DOCS_DROP&refresh=true&q=*" >/dev/null
        sleep 5
        log "reclaim deleted space"
        curl -sS -XPOST "$ES_URL/*-$TODAY/_forcemerge?only_expunge_deletes=true" >/dev/null
        sleep 30
    fi
    log "flush"
    curl -sS -XPOST "$ES_URL/*-$TODAY/_flush" >/dev/null
    sleep 5
done

log "job exited"
