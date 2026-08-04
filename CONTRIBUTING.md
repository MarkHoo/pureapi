# Contributing to PureAPI

感谢你对 PureAPI 感兴趣。这个项目希望保持轻量、清晰、零运行时依赖，因此所有贡献都应优先考虑简单性、可读性和兼容性。

## 开发环境

```bash
git clone https://github.com/MarkHoo/pureapi.git
cd pureapi
python -m pip install -e ".[dev]"
```

PureAPI 支持 Python 3.11 及以上版本。提交代码前请至少在本机当前 Python 版本上运行测试。

## 运行测试

```bash
python -m pytest
```

## 构建包

```bash
python -m build
```

构建产物会生成在 `dist/` 目录中，该目录不应提交到仓库。

## 贡献原则

- 保持核心框架零运行时依赖。
- 保持 API 行为直观，不引入过度抽象。
- 新增用户可见行为时，请同步更新 README 或 docs。
- 修改路由、请求、响应、OpenAPI 等核心行为时，请补充或更新测试。
- 避免无关格式化、重命名或大规模重排。
- 尽量使用清晰的错误信息，方便框架使用者排查问题。

## 提交前检查

```bash
python -m pytest
python -m build
```

## 发布流程

项目通过 GitHub Actions 和 PyPI Trusted Publishing 发布。

发布新版本时：

1. 更新 `pyproject.toml` 中的 `project.version`。
2. 更新 `src/pureapi/__init__.py` 中的 `__version__`。
3. 更新 `CHANGELOG.md`。
4. 提交并推送到 `main`。
5. 创建并推送版本标签，例如：

```bash
git tag v0.2.0
git push origin v0.2.0
```

推送 `v*` 标签后，GitHub Actions 会自动测试、构建并发布到 PyPI。
