variable "NAMESPACE" {
    default = "sos-mongodb"
}

variable "VERSION" {
    default = "0.0.0"
}

variable "CONTEXT_ROOT" {
    default = ""
}

variable "PLATFORM" {
    default = "default"
}

group "default" {
    targets = [
    "runtime"
    ]
}

target "runtime" {
    dockerfile = "Dockerfile"
    tags = ["${NAMESPACE}/${PLATFORM}:${VERSION}"]
    context = "${CONTEXT_ROOT}"
}
