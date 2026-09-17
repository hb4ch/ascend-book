---
title: 附录A 环境搭建
description: 从零搭建昇腾开发/验证环境
---

# 附录A 环境搭建

> 本机（写作环境）无 NPU 硬件。读者如需真机验证 `[需真机验证]` 内容，按本附录安装与验证；PTO 系列（第六编）在本机即可通过 CPU-Simulator 跑通。

## A.1 硬件与 OS 前提

- NPU：Atlas 800T A2 / 800I A3 / 900 A5 等，或对应 950 系列。
- 主机：x86_64 或 aarch64 Linux（Ubuntu 22.04/CentOS 7.6+），内核 5.10+。
- 推荐先在一张卡/一块驱动可装载的机器上开始。Driver + Toolkit 版本必须匹配。

## A.2 安装步骤

1. 下载 CANN 社区版（Toolkit、Kernel、NNAE）：https://www.hiascend.com/developer/download/community
2. 安装 driver：`./Ascend-hdk-*.run --full`（root），装完 `npu-smi info` 应能看到设备。
3. 安装 Toolkit：`./Ascend-cann-toolkit_*-linux-{arch}.run --install`，选默认路径 `/usr/local/Ascend/ascend-toolkit/latest`。
4. 安装 Kernel/算子包：`./Ascend-cann-kernels-*.run --install`。
5. 配置环境：`source /usr/local/Ascend/ascend-toolkit/set_env.sh`。
6. 验证：

```bash
npu-smi info
python -c "import torch, torch_npu; print(torch_npu.npu_count())"
python -c "import acl; print(acl.__file__)"
```

## A.3 Docker 方式

```bash
docker run --device /dev/davinci0 --device /dev/davinci_manager \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
  -v /usr/local/Ascend/ascend-toolkit:/usr/local/Ascend/ascend-toolkit \
  -v /root/.cache:/root/.cache \
  quay.io/ascend/cann:latest
```

## A.4 各仓源码构建

各仓 README 提供 `build.sh` 与依赖脚本：
- `runtime/install_deps.sh` + `runtime/build.sh`（含 UT：`pytest`/预冒烟）。
- `asc-devkit/build.sh`（cmake 构建，可进行 CPU 静态核对个算子工程）。
- `pto-isa/setup.py` / `pyproject.toml`：`pip install -e .` 后会带 CPU-Simulator 与工具链。
- `pypto/setup.py`：`pip install -e .`，需要依赖 `pto-isa` 与 llvm 工具链。
- `hcomm/build.sh`、`hixl/build.sh`、ops 系列 `build.sh`。
- 3rdparty 下载失败时用 `download_3rd_party.py` / `install_deps.sh`。

## A.5 NPU Simulator（真机替代方案）

- CANN 官方 NPU-Simulator（需 Toolkit 配套）：昇腾社区版。
- `pto-isa` 自带 CPU-Simulator：见第20章/`pto-isa/docs/getting-started_zh.md`。
- `asc-devkit` 程序可通过 simulator 编译执行（`[可用 CPU-SIM 运行]` 需要一个真实安装的 AscendC Toolkit 本身，因此本机直接标 `[需真机验证]`）。

## A.6 验证任一算子端到端

无论真机还是 simulator，验证一个算子端到端的通用五步（详见第14章）：
1. 建工程（CMakeModule）→ 2. 写 kernel/launcher → 3. 编译 → 4. 运行/比对 → 5. msprof/adump 调优。
