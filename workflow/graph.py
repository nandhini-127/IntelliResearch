
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.research_agent import research
from agents.summarizer_agent import summarize
from agents.report_agent import generate_report


# STEP 1: Define shared workflow state

class ResearchState(TypedDict, total=False):

    topic: str
    findings: list[dict]
    summary: str
    report: str
    sources: list[dict]


# STEP 2: Create Agent 1 node

def research_node(state: ResearchState):

    print("\n[Agent 1] Searching the web...")

    findings = research(state["topic"])

    print("[Agent 1] Research completed!")

    return {
        "findings": findings,
        "sources": findings
    }


# STEP 3: Create Agent 2 node

def summarize_node(state: ResearchState):

    print("\n[Agent 2] Summarizing research...")

    summary = summarize(
        state["topic"],
        state["findings"]
    )

    print("[Agent 2] Summarization completed!")

    return {
        "summary": summary
    }


# STEP 4: Create Agent 3 node

def report_node(state: ResearchState):

    print("\n[Agent 3] Generating final report...")

    report = generate_report(
        state["topic"],
        state["summary"],
        state["findings"]
    )

    print("[Agent 3] Report generation completed!")

    return {
        "report": report
    }


# STEP 5: Build the LangGraph workflow

def build_graph():

    workflow = StateGraph(ResearchState)

    # Register nodes
    workflow.add_node("research", research_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("generate_report", report_node)

    # Define execution sequence
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "summarize")
    workflow.add_edge("summarize", "generate_report")
    workflow.add_edge("generate_report", END)

    # Compile the workflow
    return workflow.compile()


# STEP 6: Compile graph
research_graph = build_graph()


# STEP 7: Execute the complete workflow

def run_research(topic: str):

    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    result = research_graph.invoke({
        "topic": topic.strip()
    })

    return result
