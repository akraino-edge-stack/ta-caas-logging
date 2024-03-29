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

FROM scratch
ADD centos-7-docker.tar.xz /
CMD ["/bin/bash"]
MAINTAINER Levente Kale <levente.kale@nokia.com>

ARG VERSION

ENV PATH /usr/share/elasticsearch/bin:$PATH
ENV JAVA_HOME /usr/lib/jvm/jre-13-openjdk
ENV DOWNLOAD_URL "https://artifacts.elastic.co/downloads/elasticsearch"
ENV ES_TARBAL "${DOWNLOAD_URL}/elasticsearch-oss-${VERSION}-linux-x86_64.tar.gz"

WORKDIR /usr/share/elasticsearch

RUN groupadd -g 202 elasticsearch \
&&  adduser -u 202 -g 202 -d /usr/share/elasticsearch elasticsearch \
&&  yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
&&  yum install -y --setopt=skip_missing_names_on_install=False \
      java-latest-openjdk-headless \
      unzip \
      which \
      coreutils \
      cronie \
      supervisor \
&&  yum clean all \
&&  curl -fsSL ${ES_TARBAL} | tar zx --strip-components=1 \
&&  chown -R elasticsearch:elasticsearch /usr/share/elasticsearch \
# workaround for Elasticsearch: this way ES can list the used plugins, and remove the jdk folder (open jdk slimmer)
&&  cp -al /usr/share/elasticsearch/modules/* /usr/share/elasticsearch/plugins/ \
&&  rm -rf /usr/share/elasticsearch/jdk \
# workaround end
&&  sed '/GC logging/Q' -i /usr/share/elasticsearch/config/jvm.options   # disable GC logging

COPY elasticsearch-logrotate.sh /etc/cron.hourly/
COPY elasticsearch-setindex.sh /usr/share/elasticsearch/
COPY log4j2.properties /usr/share/elasticsearch/config/
COPY supervisord.conf /etc/
