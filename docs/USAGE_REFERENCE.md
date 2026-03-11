# cube 模块严格使用文档

本文档约定：所有 API 以 `cube.py` 为准；示例均在项目根目录下以 `python -c "..."` 或脚本形式可运行。

---

## 1. 导入与约定

### 1.1 推荐导入方式

```python
# 方式一：按需导入（推荐）
from cube import (
    CubeState,
    MOVES,
    apply_move,
    apply_algorithm,
    parse_algorithm,
    get_algorithm_permutation,
    permutation_cycles,
    format_cycles,
    analyze_algorithm,
)

# 方式二：群论与位置过滤
from cube import (
    get_algorithm_parity,
    get_algorithm_order,
    invert_algorithm,
    compose_algorithms,
    commutator,
    conjugate,
    is_three_cycle_algorithm,
    enumerate_commutator_three_cycles,
    sample_commutators,
    classify_conjugacy_classes,
    commutator_conjugacy_statistics,
    CORNER_TOP,
    EDGE_TOP,
    CORNER_BOTTOM,
    EDGE_BOTTOM,
    CORNER_FRONT,
    EDGE_FRONT,
    CORNER_ALL,
    EDGE_ALL,
)
```

### 1.2 编码约定

- **角块位置**：0–7，对应 UFR, UFL, UBL, UBR, DFR, DFL, DBL, DBR。
- **棱块位置**：0–11，对应 UF, UL, UB, UR, FR, FL, BL, BR, DF, DL, DB, DR。
- **角块朝向**：0/1/2 (mod 3)。**棱块朝向**：0/1 (mod 2)。合法状态满足角块朝向和≡0 (mod 3)、棱块朝向和≡0 (mod 2)。

---

## 2. 状态与操作

### 2.1 CubeState

- **构造**：`CubeState(corners=None, edges=None, corner_ori=None, edge_ori=None)`  
  默认即还原态；列表长度分别为 8、12、8、12。
- **方法**：`copy()`、`is_solved()`。

**示例：初始状态与复制**

```python
from cube import CubeState, apply_move, MOVES

s = CubeState()
assert s.is_solved()

s2 = s.copy()
s2 = apply_move(s2, MOVES["F"])
assert not s2.is_solved()
assert s.is_solved()  # 原状态未变
```

### 2.2 单步操作 apply_move

- **签名**：`apply_move(state: CubeState, move: Move) -> CubeState`
- **说明**：返回新状态，不修改 `state`。

**示例：F 四次回到恒等**

```python
from cube import CubeState, apply_move, MOVES

s = CubeState()
for _ in range(4):
    s = apply_move(s, MOVES["F"])
assert s.is_solved()
```

---

## 3. 公式解析与执行

### 3.1 parse_algorithm

- **签名**：`parse_algorithm(alg_str: str) -> List[str]`
- **支持**：单步 F/R/U/L/B/D、逆 F'/R' 等、双层 F2 等、交换子 `[A, B]`、嵌套 `[A, [B, C]]`。

**示例**

```python
from cube import parse_algorithm

assert parse_algorithm("F R U R' U' F'") == ["F", "R", "U", "R'", "U'", "F'"]
assert parse_algorithm("[R, U]") == ["R", "U", "R'", "U'"]
```

### 3.2 apply_algorithm

- **签名**：`apply_algorithm(state: CubeState, alg_str: str) -> CubeState`

**示例**

```python
from cube import CubeState, apply_algorithm

s = apply_algorithm(CubeState(), "F F F F")
assert s.is_solved()
```

### 3.3 get_algorithm_permutation

- **签名**：`get_algorithm_permutation(alg_str: str) -> Tuple[List[int], List[int]]`
- **返回**：`(角块置换, 棱块置换)`，均为长度 8 与 12 的列表。

**示例**

```python
from cube import get_algorithm_permutation, permutation_cycles, format_cycles

cp, ep = get_algorithm_permutation("R U R' U'")
print("角块循环:", format_cycles(permutation_cycles(cp)))
print("棱块循环:", format_cycles(permutation_cycles(ep)))
```

---

## 4. 置换与循环

### 4.1 置换运算

- `apply_permutation(state: List[int], perm: List[int]) -> List[int]`  
  语义：`result[i] = state[perm[i]]`。
- `compose_permutation(p, q)`  
  先应用 `p` 再应用 `q`。
- `invert_permutation(p)`  
  逆置换。

### 4.2 permutation_cycles / format_cycles

- **签名**：`permutation_cycles(perm: List[int]) -> List[Tuple[int, ...]]`  
  返回非平凡循环列表。
- **签名**：`format_cycles(cycles) -> str`  
  可读字符串，如 `(0 4 5 1) (2 3)`。

**示例**

```python
from cube import permutation_cycles, format_cycles, MOVES

c_cycles = permutation_cycles(MOVES["F"].corner_perm)
e_cycles = permutation_cycles(MOVES["F"].edge_perm)
print("F 角块:", format_cycles(c_cycles))  # (0 4 5 1)
print("F 棱块:", format_cycles(e_cycles))  # (0 4 8 5)
```

---

## 5. 群论基础

### 5.1 奇偶性 get_algorithm_parity

- **签名**：`get_algorithm_parity(alg_str: str) -> Tuple[int, int, int]`
- **返回**：`(角块奇偶, 棱块奇偶, 总奇偶)`，0=偶、1=奇。

**示例**

```python
from cube import get_algorithm_parity

c_par, e_par, total = get_algorithm_parity("R U R' U'")
print("角块:", "偶" if c_par == 0 else "奇")
print("棱块:", "偶" if e_par == 0 else "奇")
print("整体:", "偶" if total == 0 else "奇")
```

### 5.2 元素阶 get_algorithm_order

- **签名**：`get_algorithm_order(alg_str: str, max_power: int = 1000) -> int`
- **返回**：最小正整数 n 使得公式^n 为恒等（含朝向）；未在 `max_power` 内则返回 -1。

**示例**

```python
from cube import get_algorithm_order

print(get_algorithm_order("F"))       # 4
print(get_algorithm_order("R U R' U'"))  # 6
```

### 5.3 逆与复合

- `invert_algorithm(alg_str: str) -> str`  
  公式的逆（字符串）。
- `compose_algorithms(*alg_strs: str) -> str`  
  从左到右依次复合。

**示例**

```python
from cube import invert_algorithm, compose_algorithms, apply_algorithm, CubeState

inv = invert_algorithm("F R")
# inv 为 "R' F'"
s = apply_algorithm(CubeState(), compose_algorithms("F R", inv))
assert s.is_solved()
```

### 5.4 交换子 commutator

- **签名**：`commutator(alg_a: str, alg_b: str) -> str`
- **定义**：[A, B] = A B A⁻¹ B⁻¹。

**示例**

```python
from cube import commutator, get_algorithm_permutation, permutation_cycles, format_cycles

alg = commutator("R", "U")
cp, ep = get_algorithm_permutation(alg)
print("公式:", alg)
print("角块:", format_cycles(permutation_cycles(cp)))
print("棱块:", format_cycles(permutation_cycles(ep)))
```

### 5.5 共轭 conjugate

- **签名**：`conjugate(alg_x: str, alg_a: str) -> str`
- **定义**：x A x⁻¹。

**示例**

```python
from cube import conjugate

# 把 [R,U] 用 F 共轭到“前面”
alg = conjugate("F", "R U R' U'")
print(alg)  # F R U R' U' F'
```

---

## 6. 位置集合常量（位置过滤）

以下常量用于 `is_three_cycle_algorithm`、`enumerate_commutator_three_cycles` 的 `allowed_corners` / `allowed_edges`。传入 `None` 表示不限制该部分。

| 常量 | 含义 | 角/棱 |
|------|------|--------|
| CORNER_TOP    | 顶层四角 0,1,2,3 | 角 |
| CORNER_BOTTOM | 底层四角 4,5,6,7 | 角 |
| CORNER_FRONT  | 前层四角         | 角 |
| CORNER_BACK   | 后层四角         | 角 |
| CORNER_RIGHT  | 右层四角         | 角 |
| CORNER_LEFT   | 左层四角         | 角 |
| EDGE_TOP      | 顶层四棱 0,1,2,3 | 棱 |
| EDGE_BOTTOM   | 底层四棱 8,9,10,11 | 棱 |
| EDGE_FRONT / EDGE_BACK / EDGE_RIGHT / EDGE_LEFT | 各面四棱 | 棱 |
| CORNER_ALL / EDGE_ALL | 全部 0..7 / 0..11 | 角/棱 |

**示例：仅允许顶层角与顶层棱**

```python
from cube import CORNER_TOP, EDGE_TOP, enumerate_commutator_three_cycles

results = enumerate_commutator_three_cycles(
    allowed_corners=CORNER_TOP,
    allowed_edges=EDGE_TOP,
)
for r in results:
    print(r["alg"], r["corner_cycles"], r["edge_cycles"])
```

---

## 7. 三循环判定与枚举

### 7.1 is_three_cycle_algorithm

- **签名**：  
  `is_three_cycle_algorithm(alg_str, part='any', pure=False, allowed_corners=None, allowed_edges=None) -> bool`
- **参数**：
  - `part`：`'corner'` | `'edge'` | `'both'` | `'any'`，限定考察角/棱/两者/任一。
  - `pure`：是否要求“纯三循环”（该部分仅一个 3-循环，其余不动）。
  - `allowed_corners` / `allowed_edges`：允许的位置编号列表；`None` 表示不限制。所有非平凡循环中的位置必须落在对应白名单内。

**示例**

```python
from cube import is_three_cycle_algorithm, CORNER_TOP, CORNER_BOTTOM

# 是否有三循环（角或棱均可）
assert is_three_cycle_algorithm("R U R' U'", part="any", pure=False) is True

# 角块是否为纯三循环
assert is_three_cycle_algorithm("R U R' U'", part="corner", pure=True) is False

# 只允许顶层角参与
assert is_three_cycle_algorithm(
    "R U R' U'",
    part="corner",
    pure=False,
    allowed_corners=CORNER_TOP,
) is True
```

### 7.2 enumerate_commutator_three_cycles

- **签名**：  
  `enumerate_commutator_three_cycles(base_moves=None, nested=False, part='any', pure=False, allowed_corners=None, allowed_edges=None) -> List[Dict]`
- **返回**：字典列表，每项含 `alg`, `corner_cycles`, `edge_cycles`, `order`, `parity`。按“位置置换”去重。

**示例：仅枚举顶层角+顶层棱的三循环交换子**

```python
from cube import enumerate_commutator_three_cycles, CORNER_TOP, EDGE_TOP

results = enumerate_commutator_three_cycles(
    base_moves=["F", "R", "U", "L", "B", "D"],
    nested=False,
    part="any",
    pure=False,
    allowed_corners=CORNER_TOP,
    allowed_edges=EDGE_TOP,
)
print("个数:", len(results))
for r in results[:3]:
    print(" ", r["alg"], "阶:", r["order"], "角:", r["corner_cycles"], "棱:", r["edge_cycles"])
```

**示例：自定义位置子集（例如只动角块 0,1,3）**

```python
from cube import enumerate_commutator_three_cycles, is_three_cycle_algorithm

custom_corners = [0, 1, 3]  # UFR, UFL, UBR
custom_edges = [0, 2, 3]    # UF, UB, UR
results = enumerate_commutator_three_cycles(
    allowed_corners=custom_corners,
    allowed_edges=custom_edges,
)
# 仅会包含角块循环在 {0,1,3}、棱块循环在 {0,2,3} 内的三循环
```

---

## 8. 换向子子群与共轭类

### 8.1 sample_commutators

- **签名**：`sample_commutators(generators=None, max_word_length=2) -> List[str]`
- **说明**：用生成元及其逆生成长度 ≤ max_word_length 的单词，两两作交换子，按位置置换去重后返回公式列表。

**示例**

```python
from cube import sample_commutators

comms = sample_commutators(generators=["F", "R", "U", "L", "B", "D"], max_word_length=1)
print("交换子个数:", len(comms))
```

### 8.2 classify_conjugacy_classes

- **签名**：`classify_conjugacy_classes(algs: List[str], conjugators=None) -> List[Dict]`
- **返回**：每个共轭类一个字典：`representative`, `size`, `corner_cycles`, `edge_cycles`, `order`, `parity`（含 corner/edge/total）。

**示例**

```python
from cube import sample_commutators, classify_conjugacy_classes

comms = sample_commutators(max_word_length=1)
classes = classify_conjugacy_classes(comms, conjugators=["F", "R", "U", "L", "B", "D"])
print("共轭类个数:", len(classes))
for cls in classes[:2]:
    print("  代表元:", cls["representative"])
    print("  类大小:", cls["size"], "阶:", cls["order"])
```

### 8.3 commutator_conjugacy_statistics

- **签名**：`commutator_conjugacy_statistics(generators=None, max_word_length=1) -> List[Dict]`
- **说明**：先 `sample_commutators`，再 `classify_conjugacy_classes`，返回共轭类统计。

**示例**

```python
from cube import commutator_conjugacy_statistics

stats = commutator_conjugacy_statistics(generators=["F", "R", "U", "L", "B", "D"], max_word_length=1)
for s in stats:
    print(s["representative"], "size:", s["size"], "order:", s["order"])
```

---

## 9. 分析与验证

### 9.1 check_orientation_valid

- **签名**：`check_orientation_valid(state: CubeState) -> Tuple[bool, str]`
- **返回**：`(是否合法, 说明字符串)`。

**示例**

```python
from cube import CubeState, apply_algorithm, check_orientation_valid

s = apply_algorithm(CubeState(), "F R U R' U' F'")
ok, msg = check_orientation_valid(s)
print(ok, msg)
```

### 9.2 analyze_algorithm

- **签名**：`analyze_algorithm(alg_str: str) -> None`
- **说明**：打印公式展开、角/棱置换与循环、朝向、奇偶性、元素阶、朝向合法性及是否恒等。

**示例**

```python
from cube import analyze_algorithm

analyze_algorithm("F R U R' U' F'")
analyze_algorithm("[R, U]")
```

---

## 10. 完整示例脚本

下面脚本可直接保存为 `examples/usage_demo.py` 运行，用于自检环境与 API。

```python
#!/usr/bin/env python3
"""cube 模块使用示例（对应 USAGE_REFERENCE.md）"""
from cube import (
    CubeState,
    MOVES,
    apply_move,
    apply_algorithm,
    parse_algorithm,
    get_algorithm_permutation,
    permutation_cycles,
    format_cycles,
    get_algorithm_parity,
    get_algorithm_order,
    invert_algorithm,
    commutator,
    conjugate,
    is_three_cycle_algorithm,
    enumerate_commutator_three_cycles,
    CORNER_TOP,
    EDGE_TOP,
    check_orientation_valid,
    analyze_algorithm,
)

def main():
    # 状态与单步
    s = CubeState()
    s = apply_move(s, MOVES["F"])
    assert not s.is_solved()
    s = apply_algorithm(CubeState(), "F F F F")
    assert s.is_solved()

    # 公式与置换
    moves = parse_algorithm("[R, U]")
    assert len(moves) == 4
    cp, ep = get_algorithm_permutation("R U R' U'")
    print("R U R' U' 角块循环:", format_cycles(permutation_cycles(cp)))
    print("R U R' U' 棱块循环:", format_cycles(permutation_cycles(ep)))

    # 群论
    print("奇偶性:", get_algorithm_parity("R U R' U'"))
    print("阶:", get_algorithm_order("F"), get_algorithm_order("R U R' U'"))
    inv = invert_algorithm("F R")
    assert apply_algorithm(CubeState(), "F R " + inv).is_solved()
    print("交换子 [R,U]:", commutator("R", "U"))
    print("共轭 F(R U R' U')F':", conjugate("F", "R U R' U'"))

    # 三循环与位置过滤
    assert is_three_cycle_algorithm("R U R' U'", part="any") is True
    results = enumerate_commutator_three_cycles(
        allowed_corners=CORNER_TOP,
        allowed_edges=EDGE_TOP,
    )
    print("顶层角+顶层棱三循环交换子个数:", len(results))

    # 朝向与综合分析
    s = apply_algorithm(CubeState(), "F R U R' U' F'")
    ok, msg = check_orientation_valid(s)
    print("朝向合法:", ok, msg)
    print("--- analyze_algorithm 输出 ---")
    analyze_algorithm("F R U R' U' F'")
    print("--- 示例结束 ---")

if __name__ == "__main__":
    main()
```

---

## 11. 参考

- 位置与朝向编码细节见 [ENCODING_REFERENCE.md](ENCODING_REFERENCE.md)。
- 操作列表与循环见 [MOVES_REFERENCE.md](MOVES_REFERENCE.md)。
- 文档索引见 [DOCS_INDEX.md](DOCS_INDEX.md)。
