//侧边栏
// github: https://github.com/MaLunan/vuepress-sidebar-atuo/blob/main/index.js
// const autosidebar = require('vuepress-auto-sidebar-doumjun')
import {readdirSync, statSync} from 'fs'
import {join} from 'path'
export function getChildren(path, sort=true) {
    console.info("----------------------------------------------------------")
    console.info(path)
    let root = []
    readDirSync(path, root)
    root = root.map(item=>{
        if (item.split('/')[6]){
            return item.split('/')[6]
        }
        else if (item.split('/')[5]){
            return item.split('/')[5]
        } else if (item.split('/')[4]){
            return item.split('/')[4]
        } else if (item.split('/')[3]){
            return item.split('/')[3]
        } else {
            return item.split('/')[2]
        }
    })
    
    //排序
    if (sort) {
        let sortList=[]
        let nosortList=[]
        root.forEach(item=>{
            // 如果文件夹或文件名最后包含 “temp” 关键字，则不参与菜单栏的生成
            // 如 01.eureka_practice.md-temp、eureka-temp
            if (item.match(/.*temp/)) {
                console.info(item)
                nosortList.push(item)
            } else {
                sortList.push(item)
            }

            
        })
        root = sortList.sort(function(a,b){
            return a.replace(".md","")-b.replace(".md","")
        })
    }
    console.info("--------------- 开始打印目录---------------")
    console.info(root)
    console.info("--------------- 完成打印目录---------------\r\n")
    return root
}
function readDirSync(path,root){
    var pa = readdirSync(path);
    pa.forEach(function(ele, index){
    var info = statSync(path+"/"+ele)
    if(info.isDirectory()) {
        readDirSync(path+ele,root)
    } else {
        if (checkFileType(ele)) {
            root.push(prefixPath(path,ele))
        }
        }
    })
}
function checkFileType(path) {
    return path.includes(".md")
}
function prefixPath(basePath, dirPath) {
    let index = basePath.indexOf("/")
    // 去除一级目录地址
    basePath = basePath.slice(index, basePath.length)
    // replace用于处理windows电脑的路径用\表示的问题
    return join(basePath,dirPath).replace(/\\/g,"/")
}
