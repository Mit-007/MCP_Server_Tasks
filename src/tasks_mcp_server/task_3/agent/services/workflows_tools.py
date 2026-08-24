from langchain.tools import tool
from src.tasks_mcp_server.task_3.agent.workflows import wf5_stats_report_generate as wf5
from src.tasks_mcp_server.task_3.agent.workflows import (
    wf1_link_job_and_call as wf1,
    wf2_failed_calls_bulk_update_jobs as wf2,
    wf3_create_follow_up_jobs as wf3,
    wf4_pending_calls_jobs_mapping as wf4,
    wf5_stats_report_generate as wf5
)
from src.tasks_mcp_server.task_3.agent.core.logger import logger

class WorkflowToolsRegistry:
    """Manages workflow tools and their descriptions"""
    
    def __init__(self, tools_by_name: dict):
        self.tools_by_name = tools_by_name
        self.workflow_tools = {}
        self._register_workflows()
    
    def _register_workflows(self):
        """Register all workflows as tools"""
        
        # Workflow 1: Link job and call
        @tool
        async def wf1_link_call_job(transcript: str):
            """
            [WORKFLOW] Create a customer call log, create a related job, 
            and link them together with a call note.
            
            Use this when you need to:
            - Log a customer call
            - Create a service job from the call
            - Link the job to the call record
            
            Args:
                transcript: Full transcript of the customer call
                
            Returns:
                dict with keys: call, job, note (all created items)
            """
            logger.info("Executing Workflow 1: Link Job and Call")
            return await wf1.link_job_and_call_workflow.ainvoke({
                "transcript": transcript,
                "tools_by_name": self.tools_by_name,
            })
        
        # Workflow 2: Failed calls to job updates
        @tool
        async def wf2_match_failed_calls_jobs():
            """
            [WORKFLOW] Find all failed calls, extract job IDs from notes, 
            and cancel those jobs.
            
            Use this when you need to:
            - Process failed calls
            - Identify related jobs
            - Auto-cancel jobs linked to failed calls
            
            Returns:
                dict with keys: cancelled_job_ids, updated_jobs
            """
            logger.info("Executing Workflow 2: Match Failed Calls and Update Jobs")
            return await wf2.match_failed_calls_jobs_update_workflow.ainvoke({
                "tools_by_name": self.tools_by_name,
            })
        
        # Workflow 3: Create follow-up jobs
        @tool
        async def wf3_create_followups():
            """
            [WORKFLOW] Analyze pending jobs and create follow-up jobs 
            based on customer needs.
            
            Use this when you need to:
            - Generate follow-up tasks
            - Proactively create jobs for pending items
            
            Returns:
                dict with created follow-up jobs
            """
            logger.info("Executing Workflow 3: Create Follow-up Jobs")
            return await wf3.create_follow_up_jobs_workflow.ainvoke({
                "tools_by_name": self.tools_by_name,
            })
        
        # Workflow 4: Pending calls to jobs mapping
        @tool
        async def wf4_map_pending_calls():
            """
            [WORKFLOW] Match pending calls to open jobs and create 
            relationships.
            
            Use this when you need to:
            - Link pending calls to jobs
            - Map customer interactions to service requests
            
            Returns:
                dict with mapping results
            """
            logger.info("Executing Workflow 4: Map Pending Calls to Jobs")
            return await wf4.pending_calls_jobs_mapping_workflow.ainvoke({
                "tools_by_name": self.tools_by_name,
            })
        
        # Workflow 5: Generate stats report
        @tool
        async def wf5_generate_stats():
            """
            [WORKFLOW] Generate a comprehensive statistics report 
            on calls and jobs.
            
            Use this when you need to:
            - Get performance metrics
            - View call/job statistics
            - Generate reports
            
            Returns:
                dict with statistics and report data
            """
            logger.info("Executing Workflow 5: Generate Statistics Report")
            return await wf5.call_stats_job_impact_report_workflow.ainvoke({
                "tools_by_name": self.tools_by_name,
            })
        
        # Store tools
        self.workflow_tools = {
            "wf1_link_call_job": wf1_link_call_job,
            "wf2_match_failed_calls_jobs": wf2_match_failed_calls_jobs,
            "wf3_create_followups": wf3_create_followups,
            "wf4_map_pending_calls": wf4_map_pending_calls,
            "wf5_generate_stats": wf5_generate_stats,
        }
    
    def get_workflow_tools(self) -> list:
        """Return list of workflow tools"""
        return list(self.workflow_tools.values())
    
    def get_workflow_tools_dict(self) -> dict:
        """Return dict of workflow tools by name"""
        return self.workflow_tools