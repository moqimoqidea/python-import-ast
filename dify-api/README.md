# [dify-api](https://github.com/langgenius/dify/tree/main/api)

分析 dify 项目 api 下的依赖关系

## 当前结论

经过排除外部依赖，得到如下依赖关系：

- configs: 不依赖其他目录
- constants: models
- controllers: configs, constants, core, events, extensions, fields, libs, models, services, tasks
- core: configs, constants, events, extensions, libs, models, services, tasks
- events: core, models, tasks
- extensions: core, libs, schedule
- fields: libs
- libs: core, extensions, models
- migrations: models
- models: configs, core, extensions, libs
- schedule: configs, core, extensions, models
- services: configs, constants, core, events, extensions, libs, models, tasks
- tasks: configs, core, extensions, libs, models, services
- tests: configs, core, extensions, libs, models, services

## 运行命令

以 configs 目录为例，运行命令为：

```shell
python ast-import.py \
  --ignore-local \
  --ignore-relative \
  --path /Users/moqi/code/dify/api/configs > dify-api-dependencies-configs.txt
```
