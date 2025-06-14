# 🐧 WSL2メモ（Windows Subsystem for Linux v2）

## 📌 概要
- **WSL2** は Windows で本格的な Linux 環境を動かせる仕組み
- 仮想化ベースでフル機能の Linux カーネルを使用
- Docker などのツールもネイティブに動作する

---

## 🛠️ WSL2 インストール手順（初回のみ）

### Windows 10 / 11 共通（PowerShellを「管理者」として実行）

```powershell
wsl --install
```

## 起動方法
```cmd
wsl                # 既定のディストリビューションを起動
wsl -d Ubuntu      # 特定のディストリビューションを起動
```

## エクスプローラーからLinuxのファイルにアクセス
```
\\wsl$\Ubuntu\
```
