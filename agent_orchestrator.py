#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 调用器 - Agent Orchestrator
用于管理和调用各种自定义 Agent
"""

import json
import subprocess
from pathlib import Path


class AgentOrchestrator:
    """Agent 编排器"""
    
    def __init__(self):
        """初始化 Agent 编排器"""
        self.agents_dir = Path(__file__).parent / 'agents'
        self.loaded_agents = {}
        
    def load_agent(self, agent_name):
        """
        加载指定的 Agent
        
        Args:
            agent_name (str): Agent 名称
            
        Returns:
            dict: Agent 配置信息
        """
        agent_file = self.agents_dir / f"{agent_name}.agent.json"
        
        if not agent_file.exists():
            return {'error': f'Agent {agent_name} 不存在'}
        
        with open(agent_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.loaded_agents[agent_name] = config
        return config
    
    def list_agents(self):
        """列出所有可用的 Agents"""
        agents = []
        for agent_file in self.agents_dir.glob('*.agent.json'):
            with open(agent_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                agents.append({
                    'name': config['agent_name'],
                    'type': config['agent_type'],
                    'description': config['description']
                })
        return agents
    
    def execute_agent(self, agent_type, file_path, output_format='text'):
        """
        执行指定的 Agent
        
        Args:
            agent_type (str): Agent 类型
            file_path (str): 文件路径
            output_format (str): 输出格式
            
        Returns:
            str: 执行结果
        """
        # 找到对应的 Agent 配置文件
        agent_config = None
        for agent_file in self.agents_dir.glob('*.agent.json'):
            with open(agent_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if config['agent_type'] == agent_type:
                    agent_config = config
                    break
        
        if not agent_config:
            return f"❌ 未找到类型为 {agent_type} 的 Agent"
        
        # 构建执行命令
        command = agent_config['execution_command'].split() + [file_path, output_format]
        
        try:
            # 执行命令
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"❌ 执行失败：{e.stderr}"
        except Exception as e:
            return f"❌ 异常：{str(e)}"
    
    def find_matching_agent(self, user_query):
        """
        根据用户查询找到匹配的 Agent
        
        Args:
            user_query (str): 用户查询
            
        Returns:
            str: 匹配的 Agent 类型，如果没有则返回 None
        """
        query_lower = user_query.lower()
        
        for agent_file in self.agents_dir.glob('*.agent.json'):
            with open(agent_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                keywords = config.get('trigger_keywords', [])
                
                for keyword in keywords:
                    if keyword.lower() in query_lower:
                        return config['agent_type']
        
        return None


def main():
    """主函数"""
    orchestrator = AgentOrchestrator()
    
    # 列出所有可用的 Agents
    print("🤖 可用的 Agents:")
    print("=" * 60)
    agents = orchestrator.list_agents()
    for agent in agents:
        print(f"\n名称：{agent['name']}")
        print(f"类型：{agent['type']}")
        print(f"描述：{agent['description']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
