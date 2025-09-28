FROM node:20-slim as development-stage

# SET WORKING DIRECTORY
WORKDIR /app

# Copy runtime script & make it executable
COPY /docker/client/entrypoint.sh /entrypoint.sh

COPY ./client/package.json ./client/package-lock.json ./

# Install ALL Dependencies
RUN npm install

# Accept build arg
ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=$NEXT_PUBLIC_BACKEND_URL

# Copy Application code into a directory called `app`
COPY ./client /app

RUN npm run build

# ========================================
# ---- Executed at Container Runtime ----
# ========================================

# CMD commands get executed at container runtime!
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]