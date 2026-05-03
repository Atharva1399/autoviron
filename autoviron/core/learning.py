from autoviron.ux.console import console

# Simulated AI Knowledge Base
PACKAGE_KNOWLEDGE = {
    "requests": "A simple, elegant HTTP library for Python, built for human beings. It allows you to send HTTP/1.1 requests extremely easily.",
    "fastapi": "A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
    "django": "A high-level Python web framework that encourages rapid development and clean, pragmatic design.",
    "pandas": "A fast, powerful, flexible and easy to use open source data analysis and manipulation tool.",
    "numpy": "The fundamental package for scientific computing with Python. It provides a multidimensional array object.",
    "scikit-learn": "Simple and efficient tools for predictive data analysis, built on NumPy, SciPy, and matplotlib.",
    "beautifulsoup4": "A library for pulling data out of HTML and XML files. It provides idiomatic ways of navigating, searching, and modifying the parse tree.",
    "uvicorn": "A lightning-fast ASGI server implementation, using uvloop and httptools. It runs async web frameworks like FastAPI.",
    "pytest": "A framework that makes building simple and scalable tests easy.",
}

def explain_dependency(package_name: str):
    """Explain what a package does and why it is typically used."""
    package_name = package_name.lower()
    
    console.print(f"\n[bold magenta]Learning Mode: {package_name}[/bold magenta]")
    console.print("-" * 50)
    
    explanation = PACKAGE_KNOWLEDGE.get(package_name)
    if explanation:
        console.print(f"📚 [bold]{package_name}[/bold]: {explanation}")
        console.print("\n[dim]Tip: You can use `autoviron run` to auto-install it if missing.[/dim]")
    else:
        console.print(f"🤷 AutoViron doesn't have an offline explanation for `{package_name}` yet.")
        console.print("In a future version connected to an LLM, a dynamic explanation would be generated here.")
