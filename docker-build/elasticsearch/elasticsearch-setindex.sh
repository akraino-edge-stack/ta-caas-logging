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

ack="false"
while [ "$ack" != "true" ]
do
  response=$(curl -sS -XPUT "http://localhost:$ELASTICSEARCH_LOGGING_SERVICE_PORT/_template/default_template" -H 'Content-Type: application/json' -d'
  {
    "index_patterns": ["*"],
    "settings": {
      "index": {
        "number_of_replicas": 2
      }
    }
  }')
  echo "number_of_replicas=2 has been requested";
  if [ "$response" = "{\"acknowledged\":true}" ]; then echo "number_of_replicas is set to 2"; ack="true"; fi
  sleep 1
done
