# Structure
- proto : protobuffer complier
  win64
  osx

- idl : protobuf file

for windows
```bash
# .\proto\win64\bin\protoc.exe --proto_path=.\idl --python_out=. (Get-ChildItem -Path ".\idl\compas_buff\data\*.proto" -File)
.\proto\win64\bin\protoc.exe --proto_path=.\idl --python_out=. .\idl\compas_buff\data\*.proto
```
for mac
```bash
./proto/osx/bin/protoc --proto_path=./idl --python_out=. ./idl/compas_buff/**/*.proto
```

# Install Protobuf

```bash
# Install protobuf
brew install protobuf
apt install protobuf-compiler
winget install protobuf

protoc --version
```

# Python

```bash
pip install protobuf==6.30.2

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