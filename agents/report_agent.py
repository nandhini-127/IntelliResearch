
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import get_llm
from utils.helpers import extract_text_content


def generate_report(
    topic: str,
    summary: str,
    findings: list[dict]
) -> str:

    """
    Generate a structured research report
    using the summarized research findings.
    """

    # Step 1: Initialize Gemini
    llm = get_llm()

    # Step 2: Prepare verified source references
    source_list = ""

    for i, item in enumerate(findings, start=1):

        source_list += f"""
        SOURCE {i}
        Title: {item['title']}
        URL: {item['url']}
        """

    # Step 3: Define the report generation instructions
    system_prompt = """
    You are a professional AI research report writer.

    Your responsibility is to transform research summaries
    into structured and informative research reports.

    Follow these rules:

    1. Use the supplied research summary.
    2. Do not invent facts or statistics.
    3. Do not introduce unsupported claims.
    4. Maintain a professional academic tone.
    5. Explain technical concepts clearly.
    6. Mention limitations of the available evidence.
    7. Use Markdown formatting.
    8. Do not invent references or URLs.

    Structure the report using these sections:

    # Research Report

    ## 1. Overview

    ## 2. Research Objectives

    ## 3. Key Findings

    ## 4. Detailed Analysis

    ## 5. Limitations

    ## 6. Conclusion
    """

    # Step 4: Prepare the input prompt
    user_prompt = f"""
    Research Topic:

    {topic}

    Research Summary:

    {summary}

    Available Source References:

    {source_list}

    Generate a complete and structured
    research report based on this information.

    Refer to sources using identifiers such as [S1], [S2].
    Do not create any source identifiers that do not exist.
    """

    # Step 5: Send the request to Gemini
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Step 6: Extract the report
    report = extract_text_content(response.content)

    # Step 7: Append references from actual search results
    references = "\n\n## 7. References\n\n"

    for i, item in enumerate(findings, start=1):

        references += (
            f"{i}. **[S{i}] {item['title']}**\n"
            f"   - URL: {item['url']}\n\n"
        )

    final_report = report + references

    return final_report
