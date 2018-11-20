wc -l shakespeare-macbeth-46.txt
grep -c "LADY MACBETH" shakespeare-macbeth-46.txt
grep "LADY MACBETH" shakespeare-macbeth-46.txt | grep -c "must"
grep "LADY MACBETH" shakespeare-macbeth-46.txt | grep  "blood" | cut -d ' ' -f 7
touch shake.txt
cp shakespeare-macbeth-46.txt shake.txt 
sed -i 's/LADY MACBETH/LADY GAGA/g' shake.txt
