#!/usr/bin/env bash
# 本书整理；本书无多机环境，此脚本未执行（仅 bash -n 语法核验）。
set -e   # 不加 -u：厂商 set_env.sh 可能引用未定义变量
# ①域+AllReduce 主线（样例 01；流程依其 README「编译执行」节，环境检查对应 Makefile L1-10 强制项）
CANN_SRC=/mnt/SATASSDEXT4/cann            # 本书源码基线根目录（只读，故先复制到临时目录）
source /usr/local/Ascend/cann/set_env.sh  # ←CANN 环境初始化，路径按部署改；提供 ASCEND_HOME_PATH 等
export MPI_HOME="${MPI_HOME:-/usr/local/mpich}"  # MPI 前缀，按部署改（Makefile 强制检查项）
N=8
# ↑ 01 README：RANK_SIZE 950 系产品=2、其他示例=8；实际还须 ≤ 可用 NPU 数，按环境改
test -n "${ASCEND_HOME_PATH:-}" || { echo "set_env.sh 未提供 ASCEND_HOME_PATH，请核对安装路径"; exit 1; }
test -n "${MPI_HOME:-}"         || { echo "请 export MPI_HOME=<mpi 前缀>"; exit 1; }
WK=$(mktemp -d)                            # 临时副本：源仓保持只读
cp -r "$CANN_SRC/hcomm/examples/01_communicators/01_one_device_per_process" "$WK/"
cd "$WK/01_one_device_per_process"
make && make test N="$N"                   # test 目标=mpirun -n $(N)（Makefile L52 区）；LD_LIBRARY_PATH 由目标内自加 MPI lib
# ②rank table 路线：同构替换为 02_one_device_per_process_rank_table 目录；
#   表文件按 socName 分叉（main.cc L119-121）：非 950→rank_table.json，950→rank_table_v2.json
# ③验签（条件式，源文限定）：仅当加载自编 tar 包（--vendor=cust 产物）时，
#   按对应 build 文档「关闭验签」节操作；直接用已安装 CANN 环境运行本样例，README 未要求关验签。
