pipeline {  
    agent any  
    
    tools {  
        // 定义 Jenkins 应该使用的 Git 版本  
        git 'Default'  
        nodejs "node"
    }  
    parameters {  
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: '请选择部署的分支')
        choice(name: 'ENVIRONMENT', choices: ['passjava-learning'], description: '请选择环境')
    }  

    // 定义 GitLab 仓库的 URL 和分支  
    environment {  
        GIT_URL = 'https://gitee.com/jayh2018/PassJava-Learning.git'
        SSH_URL = getSSHUrl(params.ENVIRONMENT)
    }   
  
    stages {  
        stage('获取最新代码') {  
            steps {  
                script {  
                    // 使用 params 对象获取参数值  
                    def branchName = params.GIT_BRANCH  
                    echo "Building branch: ${branchName}"  

                    echo "Building ssh url: ${SSH_URL}"  

                    // 使用 git 插件检出仓库的特定分支  
                    checkout([  
                        $class: 'GitSCM',  
                        branches: [[name: "${branchName}"]],  
                        doGenerateSubmoduleConfigurations: false,  
                        extensions: [],  
                        submoduleCfg: [],  
                        userRemoteConfigs: [[  
                            credentialsId: '2dcbf8b2-6314-4f43-8f52-79ec802f6d14', // 在 Jenkins 凭据中定义的 GitLab 凭据 ID  
                            url: "${GIT_URL}"  
                        ]]  
                    ])  
                }
            }  
        }
        stage('编译代码') {  
            steps {  
                
                script {  
                    echo "--------------- 步骤：开始编译代码 --------------- "
                    sh 'rm -rf dist.tar.gz'
                    sh 'npm install'
                    sh 'npm run docs:build'
                    sh 'tar -czf dist.tar.gz dist'
                    echo "--------------- 步骤：编译代码完成 --------------- "
                }
            }  
        }
        stage('上传代码') {  
            steps {  
                script {  
                    echo "--------------- 步骤：开始上传代码 --------------- "
                    echo "开始上传 dist 压缩包"
                    sshPublisher(
                        failOnError: true,
                        publishers: [
                            sshPublisherDesc(
                                configName: "${SSH_URL}",
                                verbose: true,
                                transfers: [
                                    sshTransfer(
                                        execCommand: '', 
                                        execTimeout: 120000, 
                                        flatten: false, 
                                        makeEmptyDirs: false, 
                                        noDefaultExcludes: false, 
                                        patternSeparator: '[, ]+', 
                                        remoteDirectory: 'passjava-learning/', 
                                        remoteDirectorySDF: false, 
                                        removePrefix: '', 
                                        sourceFiles: 'dist.tar.gz'
                                    )
                                ]
                            )
                        ]
                    )
                    echo "完成上传 JAR 包"
                    echo "--------------- 步骤：上传代码完成 --------------- "
                }
            }  
        }
        stage('更新代码') {  
            steps {  
                script {  
                    echo "--------------- 步骤：开始更新代码 --------------- "
                    sshPublisher(
                        failOnError: true,
                        publishers: [
                        sshPublisherDesc(
                            configName: "${SSH_URL}",
                            verbose: true,
                            transfers: [
                                sshTransfer(
                                    execCommand: "cd /nfs-data/passjava/passjava-learning && tar -xzf dist.tar.gz",
                                    execTimeout: 120000
                                )
                            ]
                        )
                    ])
                    echo "--------------- 步骤：更新代码完成 --------------- "
                }
            }  
        }
    }
}

def getSSHUrl(environment) {
    switch (environment) {
        case 'passjava-learning':
            return 'ubuntu@129.211.188.218'
        default:
            error "Unsupported environment: ${environment}"
    }
}