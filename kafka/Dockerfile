FROM openjdk:8-jre-alpine
ENV PATH /opt/kafka/bin:$PATH
ENV KAFKA_DIR "/opt/kafka"
ARG KAFKA_VERSION="2.13-2.7.0"

RUN apk update && apk add --no-cache bash gcompat

ADD setup/kafka_${KAFKA_VERSION}.tgz /opt

RUN ln -s /opt/kafka_${KAFKA_VERSION} ${KAFKA_DIR} 

ADD kafka-manager.sh ${KAFKA_DIR}/bin/kafka-manager

ADD conf/* ${KAFKA_DIR}/config/

ENTRYPOINT [ "kafka-manager" ]