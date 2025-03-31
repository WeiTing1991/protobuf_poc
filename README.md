# install Protobuf

```bash
# Install protobuf
brew install protobuf
apt install protobuf-compiler

protoc --version
```

# Python

```bash
# .proto to .py
protoc --proto_path=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/addressbook.proto
```

```bash
# env
python -m venv .env
source .env/bin/activate
pip install protobuf
```


# typescript

```bash
protoc \
--plugin="./node_modules/.bin/protoc-gen-ts_proto" \
--ts_out=./ts \
--proto_path=./proto/FILENAME.proto


# run test
npx tsc index.ts
node ./index.js
