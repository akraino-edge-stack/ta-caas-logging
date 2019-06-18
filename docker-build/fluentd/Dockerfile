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

FROM alpine:3.9
MAINTAINER Levente Kale <levente.kale@nokia.com>

ARG VERSION
ENV FLUENTD_VERSION=$VERSION
ENV DUMB_INIT_VERSION=1.2.2-r1
ENV SU_EXEC_VERSION=0.2-r0
ENV PATH /fluentd/.gem/ruby/2.3.0/bin:$PATH
ENV LD_PRELOAD=""

WORKDIR /fluentd

COPY entrypoint.sh /bin/

RUN apk update \
&&  apk upgrade \
&&  apk add --no-cache \
        ca-certificates \
        ruby ruby-irb \
        su-exec==${SU_EXEC_VERSION} \
        dumb-init==${DUMB_INIT_VERSION} \
&&  apk add --no-cache --virtual .build-deps \
        build-base \
        ruby-dev \
        wget \
        gnupg \
        libffi-dev \
&&  update-ca-certificates \
&&  echo 'gem: --no-document' >> /etc/gemrc \
&&  gem install oj -v 2.18.3 \
&&  gem install json -v 2.1.0 \
&&  gem install fluentd -v ${FLUENTD_VERSION} \
&&  gem install fluent-plugin-secure-forward \
&&  gem install fluent-plugin-record-reformer \
&&  gem install fluent-plugin-rewrite-tag-filter \
&&  gem install fluent-plugin-elasticsearch \
&&  gem install fluent-plugin-remote_syslog \
&&  gem install fluent-plugin-kubernetes_metadata_filter \
&&  gem install bigdecimal \
&&  gem install etc \
&&  gem install webrick \
&&  apk del .build-deps \
&&  rm -rf /var/cache/apk/* \
&&  gem sources --clear-all \
&&  rm -rf /tmp/* /var/tmp/* /usr/lib/ruby/gems/*/cache/*.gem \
&&  mkdir -p /fluentd/log \
&&  mkdir -p /fluentd/etc /fluentd/plugins \
&&  chmod +x /bin/entrypoint.sh \
&&  chmod 700 /fluentd/log
