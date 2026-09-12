FROM node:22-alpine AS deps
WORKDIR /app
COPY web/package.json web/package-lock.json* ./
RUN npm ci --omit=dev || npm install --omit=dev

FROM node:22-alpine AS build
WORKDIR /app
COPY web/package.json web/package-lock.json* ./
RUN npm ci || npm install
COPY web/ ./
# The CSV importer reads the shared alias table at runtime, so it has to be in
# the image alongside the build output.
COPY shared/ /app/shared/
RUN npm run build

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S phg && adduser -S phg -G phg
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/package.json ./package.json
COPY --from=deps  /app/node_modules ./node_modules
COPY shared/ /app/shared/
USER phg
EXPOSE 3000
CMD ["npx", "next", "start", "-p", "3000"]
