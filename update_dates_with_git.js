const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// 读取日期为2026-04-09的文件列表
const files = fs
  .readFileSync("/tmp/date_2026_files.txt", "utf8")
  .split("\n")
  .filter((line) => line.trim() !== "");

console.log(`找到 ${files.length} 个日期为2026-04-09的文件`);

let updatedCount = 0;
let skippedCount = 0;

for (const filePath of files) {
  try {
    // 读取文件内容
    const content = fs.readFileSync(filePath, "utf8");

    // 获取git提交时间
    let gitDate = "";
    try {
      // 获取文件的第一次提交时间
      const gitCmd = `git log --follow --format="%ad" --date=short "${filePath}" | tail -1`;
      gitDate = execSync(gitCmd, { encoding: "utf8" }).trim();

      if (!gitDate) {
        // 如果没有提交历史，尝试获取文件创建时间
        const stats = fs.statSync(filePath);
        const fileDate = new Date(stats.birthtime || stats.mtime);
        gitDate = fileDate.toISOString().split("T")[0];
      }
    } catch (error) {
      console.log(`无法获取 ${filePath} 的git提交时间: ${error.message}`);
      skippedCount++;
      continue;
    }

    if (!gitDate || gitDate === "2026-04-09") {
      console.log(`文件 ${filePath} 的git提交时间无效或相同: ${gitDate}`);
      skippedCount++;
      continue;
    }

    // 替换日期
    const newContent = content.replace(/date: 2026-04-09/, `date: ${gitDate}`);

    if (newContent !== content) {
      fs.writeFileSync(filePath, newContent);
      console.log(`已更新: ${filePath} -> ${gitDate}`);
      updatedCount++;
    } else {
      console.log(`无需更新: ${filePath} (日期未改变)`);
      skippedCount++;
    }
  } catch (error) {
    console.error(`处理文件 ${filePath} 时出错:`, error.message);
    skippedCount++;
  }
}

console.log(`\n处理完成！`);
console.log(`已更新: ${updatedCount} 个文件`);
console.log(`跳过: ${skippedCount} 个文件`);
