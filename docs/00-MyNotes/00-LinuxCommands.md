# Linux Commands

```bash
alias k=kubectl
find ./folder-name -type f | xargs tail -n +1

ps -aux | grep kubelet

grep -A 2 -B 2 -i image
grep -nr namespace .

... | wc -l #count lines
cat -n 

echo -n "paswrd"| base64
echo -n "bX1zcWw=" | base64 --decode
```