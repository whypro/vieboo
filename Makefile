ifeq ($(REGISTRY),)
	        REGISTRY := whypro/vieboo
	endif

ifeq ($(VERSION),)
	        VERSION := latest
	endif

IMAGE = $(REGISTRY):$(VERSION)
	IMAGE_LATEST = $(REGISTRY):latest

BUILD_ARGS=--build-arg http_proxy=http://10.0.0.12:8118 --build-arg https_proxy=https://10.0.0.12:8118

image:
	        docker build ${BUILD_ARGS} -t ${IMAGE} .
		        docker tag ${IMAGE} ${IMAGE_LATEST}
.PHONY: build

image-push:
	        docker push ${IMAGE}
.PHONY: push

image-push-latest:
	        docker push ${IMAGE_LATEST}
.PHONY: push-latest
