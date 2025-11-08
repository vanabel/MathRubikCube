# 🌐 部署到Streamlit Cloud - 详细步骤

将你的魔方模型变成任何人都可以访问的在线应用！

---

## 🎯 目标

部署后获得一个公开链接（如 `https://mathrubik.streamlit.app`），任何人都可以：
- 在浏览器中使用
- 无需安装Python或任何依赖
- 完全免费

---

## ✅ 前置条件

- [x] 代码已推送到GitHub：`https://github.com/vanabel/MathRubikCube`
- [x] 包含 `web_app.py`
- [x] 包含 `requirements.txt`

---

## 📋 部署步骤（5-10分钟）

### 步骤1：访问Streamlit Cloud

打开浏览器，访问：
```
https://streamlit.io/cloud
```

### 步骤2：登录

1. 点击右上角 **"Sign up"** 或 **"Log in"**
2. 选择 **"Continue with GitHub"**
3. 授权Streamlit访问你的GitHub账号

### 步骤3：创建新应用

1. 点击 **"New app"** 按钮
2. 填写配置：

```
Repository: vanabel/MathRubikCube
Branch: main
Main file path: web_app.py
App URL (optional): mathrubik  # 自定义名称
```

### 步骤4：高级设置（可选）

点击 **"Advanced settings"**，可以配置：

```
Python version: 3.9
```

其他保持默认即可。

### 步骤5：部署

1. 点击 **"Deploy"** 按钮
2. 等待部署（通常2-5分钟）
3. 看到部署日志和进度

### 步骤6：获取链接

部署成功后，你会获得：

```
https://mathrubik.streamlit.app
```

或

```
https://vanabel-mathrubik-web-app-xxxxx.streamlit.app
```

---

## 🎉 完成！

现在你可以：

1. **分享链接给任何人**
   - 发送给朋友、同学、老师
   - 发布在社交媒体
   - 添加到简历

2. **访问应用**
   - 在任何设备上使用
   - 无需安装
   - 实时更新

3. **管理应用**
   - 在Streamlit Cloud查看访问统计
   - 重启应用
   - 查看日志

---

## 🔧 常见问题

### Q1: 部署失败，显示"ModuleNotFoundError"

**A:** 检查 `requirements.txt`：

```txt
matplotlib>=3.3.0
streamlit>=1.28.0
```

确保所有依赖都列出了。

### Q2: 应用运行缓慢

**A:** Streamlit Cloud的免费版资源有限：
- 1 GB内存
- 共享CPU

对于本项目已足够。如需更多资源，可升级到付费版。

### Q3: 如何更新应用？

**A:** 只需推送到GitHub：

```bash
git add .
git commit -m "更新功能"
git push
```

Streamlit Cloud会自动重新部署！

### Q4: 如何自定义域名？

**A:** 
- 免费版：使用Streamlit提供的域名
- 付费版：可以绑定自定义域名

### Q5: 应用会永久运行吗？

**A:** 
- 免费版：如果7天无访问会休眠
- 访问时会自动唤醒（需等待几秒）
- 只要有人使用就会保持运行

---

## 📊 监控和管理

### 查看统计

在Streamlit Cloud控制台可以看到：
- 访问次数
- 活跃用户
- 运行时间
- 错误日志

### 重启应用

如果应用出现问题：
1. 在控制台找到应用
2. 点击 **"⋮"** 菜单
3. 选择 **"Reboot app"**

### 删除应用

1. 在控制台找到应用
2. 点击 **"⋮"** 菜单
3. 选择 **"Delete app"**

---

## 🌟 示例应用

你的应用部署后，用户可以：

1. **输入公式**
   ```
   F R U R' U' F'
   ```

2. **查看可视化**
   - 彩色魔方展开图
   - 8种颜色状态
   - 朝向符号

3. **分析数据**
   - 循环分解
   - 位置和朝向统计
   - 守恒验证

4. **使用示例**
   - 点击预设公式
   - Sexy Move
   - OLL/PLL公式
   - 交换子

---

## 🔗 进一步资源

- **Streamlit文档**: https://docs.streamlit.io
- **Streamlit社区**: https://discuss.streamlit.io
- **示例应用**: https://streamlit.io/gallery

---

## 💡 优化建议

### 提高性能

1. **缓存计算结果**
   ```python
   @st.cache_data
   def compute_state(formula):
       return apply_algorithm(CubeState(), formula)
   ```

2. **缓存图形**
   ```python
   @st.cache_data
   def render_cube(state):
       # 生成图形
       pass
   ```

### 增强功能

1. **添加公式库**
2. **添加动画效果**
3. **添加分享功能**
4. **添加历史记录导出**

---

**祝部署顺利！🚀**

**最后更新：2025-11-08**

