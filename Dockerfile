FROM alpine:3.18

ARG RESTIC_VERSION=0.16.0
ARG RESTIC_CHECKSUM=sha256:492387572bb2c4de904fa400636e05492e7200b331335743d46f2f2874150162

RUN apk --no-cache add -f \
	coreutils \
	curl \
	jq \
	unzip \
	zip \
	bzip2

ADD --checksum=${RESTIC_SHA256} https://github.com/restic/restic/releases/download/v${RESTIC_VERSION}/restic_${RESTIC_VERSION}_linux_amd64.bz2 restic.bz2

RUN bzip2 -d restic.bz2 && \
	mv restic /usr/local/bin/restic && \
	chmod +x /usr/local/bin/restic
