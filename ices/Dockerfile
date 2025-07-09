# Start with a modern Ubuntu base
FROM ubuntu:22.04

# Install build tools and required libraries for ices0
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libxml2-dev \
    libshout3-dev \
    libmp3lame-dev \
    && rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /usr/src

# Download and extract ices0
RUN wget https://downloads.us.xiph.org/releases/ices/ices-0.4.tar.gz && \
    tar -xvf ices-0.4.tar.gz

# Download modern config scripts that recognize aarch64
RUN wget -O ices-0.4/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD' && \
    wget -O ices-0.4/config.sub 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'

# Now, run the configure and build steps inside the updated directory
WORKDIR /usr/src/ices-0.4
RUN ./configure && \
    make && \
    make install

# Create the base log directory AND the channel subdirectories
RUN mkdir -p /var/log/ices/channel1 && mkdir -p /var/log/ices/channel2
RUN chmod -R 777 /var/log/ices
USER root


# The command to run when the container starts
CMD ["ices", "-c", "/etc/ices.conf"]