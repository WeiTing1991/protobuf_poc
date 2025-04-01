# Structure


# Install Protobuf
```bash
# install Protobuf

```bash
# Install protobuf
brew install protobuf
apt install protobuf-compiler

protoc --version
```

# Python

```bash
# proto to py
# protoc --proto_path=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/*.proto

# for compas_buff
# path has to be represent the same to the output directory
protoc --proto_path=./idl --python_out=. ./idl/**/*.proto
```

```bash
# venv
python3 -m venv .env 
source .env/bin/activate
pip install compas
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
