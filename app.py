
import gradio as gr

from workflow.graph import run_research


# STEP 1: Define research function

def research_topic(topic):

    if not topic or not topic.strip():
        return (
            "Please enter a research topic.",
            "",
            ""
        )

    try:

        # Execute all three agents
        result = run_research(topic.strip())

        report = result["report"]
        summary = result["summary"]

        # Prepare source links
        sources_md = ""

        for i, source in enumerate(result["sources"], start=1):

            title = source.get("title", "Source")
            url = source.get("url", "")

            if url:
                sources_md += f"{i}. [{title}]({url})\n\n"

        return (
            report,
            summary,
            sources_md
        )

    except Exception as e:

        error = f"Research failed: {str(e)}"

        return error, "", ""


# STEP 2: Create Gradio application

with gr.Blocks(
    title="IntelliResearch"
) as demo:

    gr.Markdown(
        """
        # 🔎 IntelliResearch

        ### Multi-Agent AI Research Assistant

        Enter a research topic and let our three AI agents
        search, analyze and generate a research report.
        """
    )

    # Research topic input
    topic = gr.Textbox(
        label="Research Topic",
        placeholder="Example: Recent advancements in RAG",
        lines=2
    )

    # Research button
    research_button = gr.Button(
        "Start Research",
        variant="primary"
    )

    # Output tabs
    with gr.Tab("Final Research Report"):

        report_output = gr.Markdown()

    with gr.Tab("Research Summary"):

        summary_output = gr.Markdown()

    with gr.Tab("Sources"):

        sources_output = gr.Markdown()

    # Connect button to backend
    research_button.click(
        fn=research_topic,
        inputs=topic,
        outputs=[
            report_output,
            summary_output,
            sources_output
        ]
    )

    # Also allow Enter to submit
    topic.submit(
        fn=research_topic,
        inputs=topic,
        outputs=[
            report_output,
            summary_output,
            sources_output
        ]
    )

    gr.Markdown(
        """
        ---
        **Powered by:** Gemini | Tavily | LangGraph | Gradio

        *Verify important research claims against their original sources.*
        """
    )


# STEP 3: Launch application

if __name__ == "__main__":

    demo.queue()

    demo.launch(theme=gr.themes.Soft(), server_name="127.0.0.1", server_port=7860)
