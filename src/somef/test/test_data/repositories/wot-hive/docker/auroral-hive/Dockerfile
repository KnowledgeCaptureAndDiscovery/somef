FROM eclipse-temurin:17

COPY ./log4j.properties /usr/src/wothive/log4j.properties
COPY ./schema.json /usr/src/wothive/schema.json
COPY ./self-description.json /usr/src/wothive/self-description.json
COPY ./shape.ttl /usr/src/wothive/shape.ttl
COPY ./configuration.json /usr/src/wothive/configuration.json

COPY ./wothive-*.jar /usr/src/wothive/wothive.jar

WORKDIR /usr/src/wothive

EXPOSE 9000

CMD ["java", "-jar", "./wothive.jar"]
