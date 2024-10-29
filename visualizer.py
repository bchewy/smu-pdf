import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict

class Visualizer:
    @staticmethod
    def create_structure_chart(sections: List[Dict]) -> go.Figure:
        """Create a treemap visualization of the document structure"""
        df = pd.DataFrame(sections)
        
        fig = go.Figure(go.Treemap(
            labels=[section['title'] for section in sections],
            parents=[''] * len(sections),
            values=[len(section['content'].split()) for section in sections],
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Words: %{value}<extra></extra>"
        ))
        
        fig.update_layout(
            width=800,
            height=500,
            title="Document Structure Overview",
        )
        
        return fig

    @staticmethod
    def create_length_chart(sections: List[Dict]) -> go.Figure:
        """Create a bar chart showing section lengths"""
        titles = [section['title'] for section in sections]
        lengths = [len(section['content'].split()) for section in sections]
        
        fig = go.Figure(data=[
            go.Bar(
                x=titles,
                y=lengths,
                text=lengths,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Section Word Count Distribution",
            xaxis_title="Sections",
            yaxis_title="Word Count",
            height=400
        )
        
        return fig
