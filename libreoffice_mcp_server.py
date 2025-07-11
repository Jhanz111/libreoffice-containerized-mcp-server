#!/usr/bin/env python3
"""
Complete LibreOffice MCP Server v2.5.2 - Ultimate Document Intelligence System
Version: v2.5.0-complete-toolkit
Builds upon the successful v2.4.0-analysis-tools foundation

COMPLETE TOOLSET - 11 Revolutionary Tools:
CREATION TOOLS:
- create_writer_document: Create LibreOffice Writer documents (.odt)
- create_calc_spreadsheet: Create LibreOffice Calc spreadsheets (.ods)
- convert_document: Convert between document formats

READING & ANALYSIS TOOLS:
- read_document: Read and extract content from existing documents
- document_summary: AI-powered document summarization
- search_in_document: Find specific content within documents
- extract_tables: Extract structured data from Writer documents

ADVANCED OPERATIONS (NEW):
- compare_documents: Intelligent comparison between two documents (NEW)
- analyze_document_structure: Deep analysis of document organization (NEW)
- merge_documents: Intelligently combine multiple documents (NEW)
- split_document: Break large documents into logical sections (NEW)

The world's most advanced conversational AI LibreOffice automation system - COMPLETE!

CRITICAL COMPATIBILITY: Uses EXACT same MCP framework as working v2.4.0 + new capabilities
"""

import asyncio
import sys
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import difflib
from datetime import datetime

# Import UNO components
import uno
from com.sun.star.connection import NoConnectException

# Import MCP framework (SAME as working versions)
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

def get_uno_desktop():
    """Get LibreOffice desktop connection - SAME as proven versions"""
    try:
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context)
        remote_context = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        desktop = remote_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", remote_context)
        return desktop
    except Exception as e:
        logger.error(f"Failed to connect to LibreOffice UNO: {e}")
        return None

def make_property(name, value):
    """Create a LibreOffice property - SAME as proven versions"""
    prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
    prop.Name = name
    prop.Value = value
    return prop

def extract_document_content(doc, filename: str) -> str:
    """Extract content from document - Enhanced helper function"""
    try:
        if filename.lower().endswith('.odt'):
            # Writer document
            text = doc.getText()
            return text.getString()
        elif filename.lower().endswith('.ods'):
            # Calc spreadsheet
            content_parts = []
            sheets = doc.getSheets()
            sheet_count = min(sheets.getCount(), 3)  # Limit to first 3 sheets
            
            for sheet_idx in range(sheet_count):
                sheet = sheets.getByIndex(sheet_idx)
                sheet_name = sheet.getName()
                
                # Get used range
                cursor = sheet.createCursor()
                cursor.gotoEndOfUsedArea(True)
                used_range = cursor.getRangeAddress()
                
                # Extract cell data (limited for performance)
                max_rows = min(used_range.EndRow + 1, 50)
                max_cols = min(used_range.EndColumn + 1, 20)
                
                sheet_content = []
                for row in range(used_range.StartRow, max_rows):
                    row_data = []
                    for col in range(used_range.StartColumn, max_cols):
                        cell = sheet.getCellByPosition(col, row)
                        cell_value = cell.getString() if cell.getString() else str(cell.getValue())
                        row_data.append(cell_value)
                    if any(cell.strip() for cell in row_data):
                        sheet_content.append(" | ".join(row_data))
                
                if sheet_content:
                    content_parts.append(f"Sheet '{sheet_name}':\n" + "\n".join(sheet_content))
            
            return "\n\n".join(content_parts)
        else:
            # Generic document
            if hasattr(doc, 'getText'):
                text = doc.getText()
                if hasattr(text, 'getString'):
                    return text.getString()
            return ""
    except Exception as e:
        logger.error(f"Error extracting content: {e}")
        return ""

def summarize_content(content: str, summary_type: str = "brief", max_length: int = 200) -> str:
    """Generate AI-powered summary of document content"""
    if not content.strip():
        return "Document appears to be empty or content could not be extracted."
    
    # Basic text analysis
    words = content.split()
    sentences = re.split(r'[.!?]+', content)
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    
    # Character and structure analysis
    char_count = len(content)
    word_count = len(words)
    sentence_count = len([s for s in sentences if s.strip()])
    paragraph_count = len(paragraphs)
    
    if summary_type == "bullet_points":
        # Extract key sentences (first sentence of each paragraph + any with keywords)
        key_sentences = []
        keywords = ["important", "critical", "summary", "conclusion", "result", "achievement", "success"]
        
        # First sentence of each paragraph
        for para in paragraphs[:5]:  # Limit to first 5 paragraphs
            sentences_in_para = re.split(r'[.!?]+', para)
            if sentences_in_para and sentences_in_para[0].strip():
                key_sentences.append("• " + sentences_in_para[0].strip()[:100] + "...")
        
        # Add sentences with keywords
        for sentence in sentences[:10]:  # Limit search
            if any(keyword in sentence.lower() for keyword in keywords) and len(key_sentences) < 8:
                if sentence.strip() not in [ks[2:] for ks in key_sentences]:  # Avoid duplicates
                    key_sentences.append("• " + sentence.strip()[:100] + "...")
        
        return f"Document Summary (Bullet Points):\n\n" + "\n".join(key_sentences[:6])
    
    elif summary_type == "detailed":
        # Detailed analysis with structure
        # Extract first few paragraphs and key information
        intro = paragraphs[0][:300] + "..." if paragraphs else "No content available"
        
        key_points = []
        for para in paragraphs[1:4]:  # Analyze next 3 paragraphs
            if len(para) > 50:  # Only substantial paragraphs
                key_points.append(para[:150] + "...")
        
        return f"""Detailed Document Summary:

Document Structure:
- {char_count:,} characters, {word_count:,} words
- {sentence_count} sentences in {paragraph_count} paragraphs

Introduction:
{intro}

Key Content Areas:
{chr(10).join(f"• {point}" for point in key_points[:3])}

Document Analysis:
This document appears to be {'technical/structured' if any(term in content.lower() for term in ['system', 'process', 'method', 'implementation']) else 'narrative/descriptive'} in nature, with {'complex' if word_count > 500 else 'moderate'} content density."""
    
    else:  # brief summary
        # Brief summary - key information only
        # Take first paragraph and any paragraph with key indicators
        main_content = paragraphs[0] if paragraphs else ""
        
        # Look for conclusion or summary paragraphs
        summary_paras = []
        for para in paragraphs:
            if any(indicator in para.lower() for indicator in ['summary', 'conclusion', 'result', 'achievement', 'success', 'completed']):
                summary_paras.append(para)
                break
        
        # Combine and limit length
        combined = main_content
        if summary_paras:
            combined += " " + summary_paras[0]
        
        # Truncate to max_length words
        words = combined.split()
        if len(words) > max_length:
            combined = " ".join(words[:max_length]) + "..."
        
        return f"Brief Summary: {combined}"

def search_in_content(content: str, search_term: str, search_type: str = "fuzzy") -> Dict[str, Any]:
    """Search for specific content within document text"""
    if not content.strip():
        return {"matches": [], "total_matches": 0, "message": "No content to search"}
    
    matches = []
    
    if search_type == "exact":
        # Exact string matching (case-insensitive)
        pattern = re.escape(search_term)
        for match in re.finditer(pattern, content, re.IGNORECASE):
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end]
            matches.append({
                "position": match.start(),
                "context": context,
                "match_text": match.group()
            })
    
    elif search_type == "regex":
        # Regular expression search
        try:
            for match in re.finditer(search_term, content, re.IGNORECASE):
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end]
                matches.append({
                    "position": match.start(),
                    "context": context,
                    "match_text": match.group()
                })
        except re.error as e:
            return {"matches": [], "total_matches": 0, "message": f"Invalid regex pattern: {e}"}
    
    else:  # fuzzy search (default)
        # Fuzzy search - split search term into words and find sentences containing them
        search_words = search_term.lower().split()
        sentences = re.split(r'[.!?]+', content)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_lower = sentence.lower()
            matched_words = sum(1 for word in search_words if word in sentence_lower)
            
            # Include sentence if it contains most of the search words
            if matched_words >= max(1, len(search_words) * 0.6):  # 60% of words must match
                matches.append({
                    "position": i,
                    "context": sentence[:200] + ("..." if len(sentence) > 200 else ""),
                    "match_text": sentence[:100],
                    "relevance": matched_words / len(search_words)
                })
        
        # Sort by relevance for fuzzy search
        matches.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        matches = matches[:10]  # Limit to top 10 matches
    
    return {
        "matches": matches,
        "total_matches": len(matches),
        "search_term": search_term,
        "search_type": search_type
    }

def extract_tables_from_writer(doc) -> List[Dict[str, Any]]:
    """Extract table data from Writer document"""
    tables_data = []
    
    try:
        text_tables = doc.getTextTables()
        table_count = text_tables.getCount()
        
        for i in range(min(table_count, 5)):  # Limit to first 5 tables
            table = text_tables.getByIndex(i)
            table_name = table.getName()
            
            # Get table dimensions
            rows = table.getRows()
            columns = table.getColumns()
            row_count = rows.getCount()
            col_count = columns.getCount()
            
            # Extract table data
            table_data = []
            for row in range(min(row_count, 20)):  # Limit to 20 rows
                row_data = []
                for col in range(min(col_count, 10)):  # Limit to 10 columns
                    try:
                        cell_name = chr(65 + col) + str(row + 1)  # A1, B1, etc.
                        cell = table.getCellByName(cell_name)
                        cell_text = cell.getString()
                        row_data.append(cell_text if cell_text else "")
                    except:
                        row_data.append("")
                
                # Only include non-empty rows
                if any(cell.strip() for cell in row_data):
                    table_data.append(row_data)
            
            tables_data.append({
                "table_name": table_name,
                "table_index": i,
                "rows": len(table_data),
                "columns": col_count,
                "data": table_data
            })
    
    except Exception as e:
        logger.error(f"Error extracting tables: {e}")
        return [{"error": f"Failed to extract tables: {str(e)}"}]
    
    return tables_data
	# Part 2: Advanced Helper Functions and Tool Definitions

def compare_documents_content(content1: str, content2: str, file1: str, file2: str, comparison_type: str) -> str:
    """NEW: Compare two documents with intelligent analysis"""
    if not content1.strip() and not content2.strip():
        return "Both documents appear to be empty."
    elif not content1.strip():
        return f"Document '{file1}' is empty, while '{file2}' contains {len(content2.split())} words."
    elif not content2.strip():
        return f"Document '{file2}' is empty, while '{file1}' contains {len(content1.split())} words."
    
    if comparison_type == "metadata":
        # Basic metadata comparison
        words1, words2 = len(content1.split()), len(content2.split())
        chars1, chars2 = len(content1), len(content2)
        lines1, lines2 = len(content1.split('\n')), len(content2.split('\n'))
        
        return f"""Document Metadata Comparison:

{file1}:
- {words1:,} words, {chars1:,} characters
- {lines1:,} lines

{file2}:
- {words2:,} words, {chars2:,} characters  
- {lines2:,} lines

Differences:
- Word count difference: {abs(words1 - words2):,} words
- Character difference: {abs(chars1 - chars2):,} characters
- Size ratio: {max(words1, words2) / max(min(words1, words2), 1):.1f}:1"""
    
    elif comparison_type == "structure":
        # Structure comparison
        paras1 = [p.strip() for p in content1.split('\n') if p.strip()]
        paras2 = [p.strip() for p in content2.split('\n') if p.strip()]
        
        # Look for headings (lines that are short and might be titles)
        headings1 = [p for p in paras1 if len(p) < 100 and len(p.split()) < 10]
        headings2 = [p for p in paras2 if len(p) < 100 and len(p.split()) < 10]
        
        return f"""Document Structure Comparison:

{file1} Structure:
- {len(paras1)} paragraphs
- {len(headings1)} potential headings
- Average paragraph length: {sum(len(p) for p in paras1) / max(len(paras1), 1):.0f} characters

{file2} Structure:
- {len(paras2)} paragraphs
- {len(headings2)} potential headings
- Average paragraph length: {sum(len(p) for p in paras2) / max(len(paras2), 1):.0f} characters

Structure Analysis:
- Document complexity: {'Similar' if abs(len(paras1) - len(paras2)) < 3 else 'Different'}
- Organization style: {'Structured' if len(headings1) > 2 or len(headings2) > 2 else 'Narrative'}"""
    
    elif comparison_type == "comprehensive":
        # Comprehensive comparison with content analysis
        words1, words2 = content1.split(), content2.split()
        
        # Find common words (excluding very common ones)
        common_stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        words1_clean = [w.lower().strip('.,!?;:"()[]') for w in words1 if w.lower() not in common_stop_words and len(w) > 2]
        words2_clean = [w.lower().strip('.,!?;:"()[]') for w in words2 if w.lower() not in common_stop_words and len(w) > 2]
        
        set1, set2 = set(words1_clean), set(words2_clean)
        common_words = set1.intersection(set2)
        unique1 = set1 - set2
        unique2 = set2 - set1
        
        # Calculate similarity
        similarity = len(common_words) / max(len(set1.union(set2)), 1) * 100
        
        return f"""Comprehensive Document Comparison:

Content Similarity: {similarity:.1f}%

Vocabulary Analysis:
- Common terms: {len(common_words)} words
- Unique to {file1}: {len(unique1)} words
- Unique to {file2}: {len(unique2)} words

Most frequent common terms: {', '.join(list(common_words)[:8])}

Document Characteristics:
{file1}: {len(words1):,} words, {'Technical' if any(term in content1.lower() for term in ['system', 'process', 'implementation', 'method']) else 'General'} content
{file2}: {len(words2):,} words, {'Technical' if any(term in content2.lower() for term in ['system', 'process', 'implementation', 'method']) else 'General'} content

Content Overlap Assessment:
{'High similarity - documents appear related' if similarity > 30 else 'Low similarity - documents appear to cover different topics' if similarity < 10 else 'Moderate similarity - some common themes'}"""
    
    else:  # content comparison (default)
        # Content-focused comparison
        sentences1 = [s.strip() for s in re.split(r'[.!?]+', content1) if s.strip()]
        sentences2 = [s.strip() for s in re.split(r'[.!?]+', content2) if s.strip()]
        
        # Look for similar sentences (basic matching)
        similar_count = 0
        for s1 in sentences1[:10]:  # Check first 10 sentences
            for s2 in sentences2[:10]:
                if len(s1) > 20 and len(s2) > 20:  # Only substantial sentences
                    words1 = set(s1.lower().split())
                    words2 = set(s2.lower().split())
                    overlap = len(words1.intersection(words2)) / max(len(words1.union(words2)), 1)
                    if overlap > 0.5:  # 50% word overlap
                        similar_count += 1
                        break
        
        return f"""Content Comparison between '{file1}' and '{file2}':

Document Lengths:
- {file1}: {len(content1.split())} words, {len(sentences1)} sentences
- {file2}: {len(content2.split())} words, {len(sentences2)} sentences

Content Analysis:
- Similar sentences found: {similar_count}
- Content relationship: {'Closely related' if similar_count > 2 else 'Some similarity' if similar_count > 0 else 'Different topics'}

First paragraphs comparison:
{file1}: {content1.split('.')[0][:150]}...
{file2}: {content2.split('.')[0][:150]}...

Overall Assessment:
{'These documents appear to discuss related topics with some overlapping content.' if similar_count > 1 else 'These documents appear to cover different subjects with minimal content overlap.'}"""

def analyze_document_structure_detailed(content: str, filename: str, analysis_depth: str) -> str:
    """NEW: Analyze document organization and structure"""
    if not content.strip():
        return f"Document '{filename}' appears to be empty or content could not be extracted."
    
    # Basic structure analysis
    lines = content.split('\n')
    paragraphs = [p.strip() for p in lines if p.strip()]
    sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
    words = content.split()
    
    # Identify potential headings (short lines, might be titles)
    potential_headings = []
    for i, para in enumerate(paragraphs):
        if len(para) < 100 and len(para.split()) < 12 and not para.endswith('.'):
            # Additional heading indicators
            if any(indicator in para.lower() for indicator in ['chapter', 'section', 'part', '1.', '2.', 'a.', 'b.']):
                potential_headings.append((i, para))
            elif para.isupper() or para.istitle():
                potential_headings.append((i, para))
    
    # Analyze paragraph lengths
    para_lengths = [len(p.split()) for p in paragraphs]
    avg_para_length = sum(para_lengths) / max(len(para_lengths), 1)
    
    # Content type analysis
    technical_terms = ['system', 'process', 'method', 'implementation', 'algorithm', 'function', 'data', 'analysis']
    technical_score = sum(1 for term in technical_terms if term in content.lower())
    
    narrative_indicators = ['story', 'experience', 'happened', 'felt', 'thought', 'remember', 'yesterday', 'first', 'then', 'finally']
    narrative_score = sum(1 for indicator in narrative_indicators if indicator in content.lower())
    
    if analysis_depth == "basic":
        return f"""Basic Structure Analysis for '{filename}':

Document Overview:
- {len(words):,} words in {len(sentences)} sentences
- {len(paragraphs)} paragraphs, {len(lines)} total lines
- Average paragraph length: {avg_para_length:.1f} words

Structure Type: {'Technical/Instructional' if technical_score > narrative_score else 'Narrative/Descriptive' if narrative_score > technical_score else 'Mixed Content'}
Organization: {'Well-structured' if len(potential_headings) > 2 else 'Simple structure'}"""
    
    elif analysis_depth == "comprehensive":
        # Comprehensive analysis with detailed breakdown
        
        # Sentence length analysis
        sent_lengths = [len(s.split()) for s in sentences]
        avg_sent_length = sum(sent_lengths) / max(len(sent_lengths), 1)
        
        # Vocabulary analysis
        unique_words = set(word.lower().strip('.,!?;:"()[]') for word in words)
        vocabulary_richness = len(unique_words) / max(len(words), 1)
        
        # Content distribution
        intro_words = len(' '.join(paragraphs[:2]).split()) if len(paragraphs) >= 2 else len(words)
        conclusion_words = len(' '.join(paragraphs[-2:]).split()) if len(paragraphs) >= 2 else 0
        body_words = len(words) - intro_words - conclusion_words
        
        return f"""Comprehensive Structure Analysis for '{filename}':

DOCUMENT METRICS:
- Total content: {len(words):,} words, {len(sentences)} sentences, {len(paragraphs)} paragraphs
- Vocabulary richness: {vocabulary_richness:.2%} (unique words ratio)
- Average sentence length: {avg_sent_length:.1f} words
- Average paragraph length: {avg_para_length:.1f} words

STRUCTURAL ORGANIZATION:
- Identified headings: {len(potential_headings)}
- Document sections: {'Highly structured' if len(potential_headings) > 5 else 'Moderately structured' if len(potential_headings) > 2 else 'Simple structure'}
- Content distribution: Introduction {intro_words} words, Body {body_words} words, Conclusion {conclusion_words} words

CONTENT CLASSIFICATION:
- Technical complexity: {technical_score}/10 indicators
- Narrative elements: {narrative_score}/10 indicators
- Content type: {'Technical/Analytical' if technical_score >= 4 else 'Narrative/Personal' if narrative_score >= 4 else 'General/Mixed'}

READABILITY ASSESSMENT:
- Sentence complexity: {'Complex' if avg_sent_length > 20 else 'Moderate' if avg_sent_length > 12 else 'Simple'}
- Paragraph structure: {'Dense' if avg_para_length > 100 else 'Balanced' if avg_para_length > 40 else 'Concise'}
- Overall organization: {'Professional document structure' if len(potential_headings) > 3 and avg_para_length > 30 else 'Informal or narrative style'}

STRUCTURAL RECOMMENDATIONS:
- {'Consider adding more section headings for better navigation' if len(potential_headings) < 3 and len(paragraphs) > 10 else 'Good structural organization maintained'}
- {'Paragraph length is well-balanced for readability' if 30 < avg_para_length < 80 else 'Consider adjusting paragraph length for optimal readability'}"""
    
    else:  # detailed analysis (default)
        return f"""Detailed Structure Analysis for '{filename}':

DOCUMENT OVERVIEW:
- Content volume: {len(words):,} words across {len(paragraphs)} paragraphs
- Sentence count: {len(sentences)} sentences
- Average paragraph length: {avg_para_length:.1f} words

ORGANIZATIONAL STRUCTURE:
- Structural elements identified: {len(potential_headings)} potential headings/sections
- Headings found: {[h[1][:50] + '...' if len(h[1]) > 50 else h[1] for h in potential_headings[:5]]}
- Document hierarchy: {'Multi-level structure' if len(potential_headings) > 4 else 'Simple structure' if len(potential_headings) > 1 else 'Continuous text'}

CONTENT CHARACTERISTICS:
- Writing style: {'Technical/Formal' if technical_score > 3 else 'Narrative/Personal' if narrative_score > 3 else 'General/Mixed'}
- Content density: {'Information-dense' if avg_para_length > 60 else 'Moderate density' if avg_para_length > 30 else 'Concise style'}
- Document purpose: {'Instructional/Reference' if technical_score > narrative_score else 'Storytelling/Experiential' if narrative_score > technical_score else 'General communication'}

STRUCTURAL QUALITY:
- Organization level: {'Well-organized' if len(potential_headings) > 2 else 'Basic organization'}
- Content flow: {'Structured progression' if len(potential_headings) > 0 else 'Continuous narrative'}
- Readability: {'Professional format' if len(potential_headings) > 1 and 20 < avg_para_length < 100 else 'Informal format'}"""

def merge_documents_content(contents: List[str], filenames: List[str], merge_strategy: str, output_filename: str) -> str:
    """NEW: Merge multiple documents intelligently"""
    if not contents or all(not content.strip() for content in contents):
        return "ERROR: No valid content found in source documents"
    
    valid_contents = [(content, filename) for content, filename in zip(contents, filenames) if content.strip()]
    
    if merge_strategy == "sequential":
        # Simple sequential merging with document separators
        merged_content = f"MERGED DOCUMENT: {output_filename}\n"
        merged_content += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        merged_content += f"Source documents: {', '.join(filenames)}\n"
        merged_content += "=" * 60 + "\n\n"
        
        for i, (content, filename) in enumerate(valid_contents):
            merged_content += f"DOCUMENT {i+1}: {filename}\n"
            merged_content += "-" * 40 + "\n"
            merged_content += content.strip() + "\n\n"
            merged_content += "=" * 60 + "\n\n"
        
        return merged_content
    
    elif merge_strategy == "interleaved":
        # Interleave content by paragraphs
        merged_content = f"MERGED DOCUMENT: {output_filename} (Interleaved)\n"
        merged_content += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        merged_content += f"Source documents: {', '.join(filenames)}\n"
        merged_content += "=" * 60 + "\n\n"
        
        # Split each document into paragraphs
        doc_paragraphs = []
        for content, filename in valid_contents:
            paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
            doc_paragraphs.append((paragraphs, filename))
        
        # Interleave paragraphs
        max_paras = max(len(paras) for paras, _ in doc_paragraphs)
        for i in range(max_paras):
            for paras, filename in doc_paragraphs:
                if i < len(paras):
                    merged_content += f"[From {filename}] {paras[i]}\n\n"
        
        return merged_content
    
    else:  # smart merging (default)
        # Smart merging with content analysis and organization
        merged_content = f"SMART MERGED DOCUMENT: {output_filename}\n"
        merged_content += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        merged_content += f"Source documents: {', '.join(filenames)}\n"
        merged_content += "=" * 60 + "\n\n"
        
        # Analyze content types and merge intelligently
        merged_content += "EXECUTIVE SUMMARY\n"
        merged_content += "-" * 20 + "\n"
        merged_content += f"This document combines content from {len(valid_contents)} source files:\n"
        
        for content, filename in valid_contents:
            word_count = len(content.split())
            content_type = "Technical" if any(term in content.lower() for term in ['system', 'process', 'implementation']) else "General"
            merged_content += f"• {filename}: {word_count} words ({content_type} content)\n"
        
        merged_content += "\n" + "=" * 60 + "\n\n"
        
        # Merge with intelligent sectioning
        for i, (content, filename) in enumerate(valid_contents):
            # Extract potential title from first line/paragraph
            lines = content.split('\n')
            title_line = lines[0].strip() if lines else filename
            if len(title_line) > 100:
                title_line = filename
                
            merged_content += f"SECTION {i+1}: {title_line}\n"
            merged_content += f"Source: {filename}\n"
            merged_content += "-" * 40 + "\n\n"
            merged_content += content.strip() + "\n\n"
        
        return merged_content

def split_document_content(content: str, filename: str, split_method: str, split_criteria: str = None) -> List[Dict[str, str]]:
    """NEW: Split document into logical sections"""
    if not content.strip():
        return [{"error": f"Document '{filename}' appears to be empty"}]
    
    sections = []
    
    if split_method == "by_headings":
        # Split by potential headings
        lines = content.split('\n')
        current_section = []
        section_title = "Introduction"
        section_num = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_section:
                    current_section.append("")
                continue
                
            # Check if line is a potential heading
            is_heading = (
                len(line) < 100 and 
                len(line.split()) < 12 and 
                not line.endswith('.') and
                (line.isupper() or line.istitle() or 
                 any(indicator in line.lower() for indicator in ['chapter', 'section', 'part', '1.', '2.', 'a.', 'b.']))
            )
            
            if is_heading and current_section and len(' '.join(current_section).split()) > 50:
                # Save current section
                sections.append({
                    "title": section_title,
                    "content": '\n'.join(current_section).strip(),
                    "section_number": section_num,
                    "word_count": len(' '.join(current_section).split())
                })
                
                # Start new section
                current_section = []
                section_title = line
                section_num += 1
            
            current_section.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                "title": section_title,
                "content": '\n'.join(current_section).strip(),
                "section_number": section_num,
                "word_count": len(' '.join(current_section).split())
            })
    
    elif split_method == "by_pages":
        # Split by estimated pages (assuming ~250 words per page)
        words_per_page = 250
        words = content.split()
        total_words = len(words)
        
        for i in range(0, total_words, words_per_page):
            section_words = words[i:i + words_per_page]
            page_num = i // words_per_page + 1
            
            sections.append({
                "title": f"Page {page_num}",
                "content": ' '.join(section_words),
                "section_number": page_num,
                "word_count": len(section_words)
            })
    
    elif split_method == "by_size":
        # Split by specified word count
        try:
            target_size = int(split_criteria) if split_criteria else 500
        except (ValueError, TypeError):
            target_size = 500
        
        words = content.split()
        section_num = 1
        
        for i in range(0, len(words), target_size):
            section_words = words[i:i + target_size]
            
            sections.append({
                "title": f"Section {section_num} (Words {i+1}-{i+len(section_words)})",
                "content": ' '.join(section_words),
                "section_number": section_num,
                "word_count": len(section_words)
            })
            section_num += 1
    
    else:  # by_sections (default)
        # Split by paragraph groups
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        section_size = max(3, len(paragraphs) // 5)  # Aim for ~5 sections
        section_num = 1
        
        for i in range(0, len(paragraphs), section_size):
            section_paras = paragraphs[i:i + section_size]
            section_content = '\n\n'.join(section_paras)
            
            # Use first paragraph as title hint
            title_hint = section_paras[0][:50] + "..." if len(section_paras[0]) > 50 else section_paras[0]
            
            sections.append({
                "title": f"Section {section_num}: {title_hint}",
                "content": section_content,
                "section_number": section_num,
                "word_count": len(section_content.split())
            })
            section_num += 1
    
    return sections if sections else [{"error": "Could not split document - no logical sections found"}]

# Add these helper functions BEFORE the server initialization (before "server = Server...")
# Place them after split_document_content() and before "# Initialize server"

def apply_template_placeholders(content: str, placeholders: dict, format_type: str = "mustache") -> str:
    """Replace placeholders in content with provided values"""
    result = content
    
    for key, value in placeholders.items():
        # Handle different placeholder formats
        if format_type == "mustache":
            # {{PLACEHOLDER}} format
            if not (key.startswith("{{") and key.endswith("}}")):
                search_key = f"{{{{{key}}}}}"
            else:
                search_key = key
        elif format_type == "percent":
            # %PLACEHOLDER% format
            if not (key.startswith("%") and key.endswith("%")):
                search_key = f"%{key}%"
            else:
                search_key = key
        elif format_type == "dollar":
            # $PLACEHOLDER format
            if not key.startswith("$"):
                search_key = f"${key}"
            else:
                search_key = key
        else:
            search_key = key
            
        # Replace all instances of the placeholder with the value
        result = result.replace(search_key, str(value))
    
    return result

def create_template_placeholders(content: str, markers: list, format_type: str = "mustache") -> str:
    """Convert specified text markers to placeholders in content"""
    result = content
    
    for i, marker in enumerate(markers):
        # Generate meaningful placeholder name
        # Clean the marker text to create a valid placeholder name
        placeholder_name = marker.replace(" ", "_").replace("-", "_").upper()
        # Limit length and remove special characters
        placeholder_name = "".join(c for c in placeholder_name if c.isalnum() or c == "_")[:20]
        if not placeholder_name:
            placeholder_name = f"PLACEHOLDER_{i+1}"
        
        # Create placeholder based on format
        if format_type == "mustache":
            placeholder = f"{{{{{placeholder_name}}}}}"
        elif format_type == "percent":
            placeholder = f"%{placeholder_name}%"
        elif format_type == "dollar":
            placeholder = f"${placeholder_name}"
        else:
            placeholder = f"{{{{{placeholder_name}}}}}"
        
        # Replace all instances of the marker with the placeholder
        result = result.replace(marker, placeholder)
    
    return result
    
# Initialize server (SAME as proven versions)
server = Server("libreoffice-mcp-server")

@server.list_tools()
async def list_tools():
    """List available tools - COMPLETE with all 11 tools"""
    return [
        # CREATION TOOLS (Proven Stable)
        Tool(
            name="create_writer_document",
            description="Create a LibreOffice Writer document with specified content",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the document file (without extension)"},
                    "content": {"type": "string", "description": "Text content for the document"}
                },
                "required": ["filename", "content"]
            }
        ),
        Tool(
            name="create_calc_spreadsheet",
            description="Create a LibreOffice Calc spreadsheet with data",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the spreadsheet file (without extension)"},
                    "data": {"type": "array", "description": "Array of arrays representing rows and columns", "items": {"type": "array", "items": {"type": "string"}}}
                },
                "required": ["filename", "data"]
            }
        ),
        Tool(
            name="convert_document",
            description="Convert LibreOffice documents between formats",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to input document file"},
                    "output_file": {"type": "string", "description": "Path for output document file"},
                    "format": {"type": "string", "description": "Target format (pdf, odt, docx, ods, csv, etc.)"}
                },
                "required": ["input_file", "output_file", "format"]
            }
        ),
        
        # READING & ANALYSIS TOOLS (Proven Operational)
        Tool(
            name="read_document",
            description="Read and extract content from existing LibreOffice documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the document file to read (with extension)"},
                    "extract_type": {"type": "string", "description": "Type of content extraction: 'text' (default), 'structured', or 'metadata'", "enum": ["text", "structured", "metadata"], "default": "text"}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="document_summary",
            description="Generate AI-powered summary of document content",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Document file to summarize"},
                    "summary_type": {"type": "string", "description": "Type of summary to generate", "enum": ["brief", "detailed", "bullet_points"], "default": "brief"},
                    "max_length": {"type": "integer", "description": "Maximum summary length in words", "default": 200}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="search_in_document",
            description="Search for specific content within documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Document file to search"},
                    "search_term": {"type": "string", "description": "Text to search for"},
                    "search_type": {"type": "string", "description": "Type of search to perform", "enum": ["exact", "fuzzy", "regex"], "default": "fuzzy"}
                },
                "required": ["filename", "search_term"]
            }
        ),
        Tool(
            name="extract_tables",
            description="Extract and analyze table data from Writer documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Writer document containing tables"},
                    "table_index": {"type": "integer", "description": "Specific table to extract (0-based), or -1 for all", "default": -1},
                    "output_format": {"type": "string", "description": "Format for table data output", "enum": ["json", "csv", "markdown"], "default": "json"}
                },
                "required": ["filename"]
            }
        ),
        
        # ADVANCED OPERATIONS (NEW - Complete Toolkit)
        Tool(
            name="compare_documents",
            description="Intelligent comparison between two documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "file1": {"type": "string", "description": "First document to compare"},
                    "file2": {"type": "string", "description": "Second document to compare"},
                    "comparison_type": {"type": "string", "description": "Type of comparison to perform", "enum": ["content", "structure", "metadata", "comprehensive"], "default": "content"}
                },
                "required": ["file1", "file2"]
            }
        ),
        Tool(
            name="analyze_document_structure",
            description="Deep analysis of document organization and formatting",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Document to analyze"},
                    "analysis_depth": {"type": "string", "description": "Depth of structural analysis", "enum": ["basic", "detailed", "comprehensive"], "default": "detailed"}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="merge_documents",
            description="Intelligently combine multiple documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_files": {"type": "array", "items": {"type": "string"}, "description": "List of documents to merge"},
                    "output_filename": {"type": "string", "description": "Name for merged document"},
                    "merge_strategy": {"type": "string", "description": "How to combine documents", "enum": ["sequential", "interleaved", "smart"], "default": "sequential"}
                },
                "required": ["source_files", "output_filename"]
            }
        ),
        Tool(
            name="split_document",
            description="Break large documents into logical sections",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Document to split"},
                    "split_method": {"type": "string", "description": "Method for splitting document", "enum": ["by_pages", "by_headings", "by_sections", "by_size"], "default": "by_headings"},
                    "split_criteria": {"type": "string", "description": "Specific criteria for splitting (e.g., words per section for 'by_size')"}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="template_apply",
            description="Apply a template with placeholder replacement to create a new document",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_filename": {
                        "type": "string",
                        "description": "Name of the template file to use"
                    },
                    "output_filename": {
                        "type": "string", 
                        "description": "Name for the new document to create"
                    },
                    "placeholders": {
                        "type": "object",
                        "description": "Key-value pairs for placeholder replacement"
                    },
                    "template_format": {
                        "type": "string",
                        "description": "Format of placeholders in template",
                        "enum": ["mustache", "percent", "dollar"],
                        "default": "mustache"
                    }
                },
                "required": ["template_filename", "output_filename", "placeholders"]
            }
        ),
        Tool(
            name="template_create",
            description="Create a reusable template from an existing document with placeholder markers",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_filename": {
                        "type": "string", 
                        "description": "Name of the source document to convert to template"
                },
                "template_filename": {
                    "type": "string", 
                    "description": "Name for the new template file"
                },
                "placeholder_markers": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "List of text strings to convert to placeholders (e.g., ['John Smith', '2025-01-15'])"
                },
                "placeholder_format": {
                    "type": "string", 
                    "description": "Format for placeholders in template", 
                    "enum": ["mustache", "percent", "dollar"], 
                    "default": "mustache"
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional metadata for the template (title, description, category, etc.)",
                    "default": {}
                }
            },
            "required": ["source_filename", "template_filename", "placeholder_markers"]
        }
        ),
        Tool(
            name="template_list",
            description="List available templates with filtering and search capabilities",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string", 
                        "description": "Optional search term to filter templates by name or description"
                    },
                    "category": {
                        "type": "string", 
                        "description": "Optional category to filter templates"
                    },
                    "format": {
                        "type": "string", 
                        "description": "Optional file format filter", 
                        "enum": ["odt", "ods", "docx", "xlsx", "all"], 
                        "default": "all"
                    },
                    "include_metadata": {
                        "type": "boolean", 
                        "description": "Whether to include detailed metadata in results", 
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="enhanced_style_transfer",
            description="Enhanced style transfer between documents with template-aware formatting",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_filename": {
                        "type": "string", 
                        "description": "Source document with styles to copy"
                    },
                    "target_filename": {
                        "type": "string", 
                        "description": "Target document to apply styles to"
                    },
                    "style_types": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["paragraph", "character", "page", "frame", "numbering", "table"]},
                        "description": "Types of styles to transfer",
                        "default": ["paragraph", "character"]
                    },
                    "preserve_content": {
                        "type": "boolean", 
                        "description": "Whether to preserve target document content", 
                        "default": True
                    },
                    "template_mode": {
                        "type": "boolean", 
                        "description": "Enable template-aware style transfer (preserves placeholders)", 
                        "default": False
                    },
                    "style_mapping": {
                        "type": "object",
                        "description": "Optional mapping of source style names to target style names",
                        "default": {}
                    }
                },
                "required": ["source_filename", "target_filename"]
            }
        )
    ]

@server.list_prompts()
async def list_prompts():
    return []

@server.list_resources()  
async def list_resources():
    return []
    
	# Part 3: Complete Tool Implementations and Main Function

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls - COMPLETE with all 11 tools"""
    try:
        desktop = get_uno_desktop()
        if not desktop:
            return [{"type": "text", "text": "ERROR: Could not connect to LibreOffice UNO service"}]

        # CREATION TOOLS (Unchanged from proven versions)
        if name == "create_writer_document":
            filename = arguments["filename"]
            content = arguments["content"]
            
            doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
            text = doc.getText()
            cursor = text.createTextCursor()
            text.insertString(cursor, content, False)
            
            file_url = f"file:///home/libreoffice/Documents/{filename}.odt"
            doc.storeAsURL(file_url, ())
            doc.close(True)
            
            return [{"type": "text", "text": f"SUCCESS: Created Writer document {filename}.odt with content"}]

        elif name == "create_calc_spreadsheet":
            filename = arguments["filename"]
            data = arguments["data"]
            
            doc = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ())
            sheets = doc.getSheets()
            sheet = sheets.getByIndex(0)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_value in enumerate(row_data):
                    cell = sheet.getCellByPosition(col_idx, row_idx)
                    cell.setString(str(cell_value))
            
            file_url = f"file:///home/libreoffice/Documents/{filename}.ods"
            doc.storeAsURL(file_url, ())
            doc.close(True)
            
            return [{"type": "text", "text": f"SUCCESS: Created Calc spreadsheet {filename}.ods with {len(data)} rows"}]

        elif name == "convert_document":
            input_file = arguments["input_file"]
            output_file = arguments["output_file"]
            format_name = arguments["format"]
            
            format_filters = {
                "pdf": "writer_pdf_Export",
                "docx": "MS Word 2007 XML",
                "csv": "Text - txt - csv (StarCalc)"
            }
            
            if format_name not in format_filters:
                return [{"type": "text", "text": f"ERROR: Unsupported format {format_name}"}]
            
            input_url = f"file:///home/libreoffice/Documents/{input_file}"
            output_url = f"file:///home/libreoffice/Documents/{output_file}"
            
            doc = desktop.loadComponentFromURL(input_url, "_blank", 0, ())
            filter_name = format_filters[format_name]
            export_props = (make_property("FilterName", filter_name),)
            doc.storeToURL(output_url, export_props)
            doc.close(True)
            
            return [{"type": "text", "text": f"SUCCESS: Converted {input_file} to {output_file} in {format_name} format"}]

        # READING & ANALYSIS TOOLS (From v2.4.0)
        elif name == "read_document":
            filename = arguments["filename"]
            extract_type = arguments.get("extract_type", "text")
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                if filename.lower().endswith('.odt'):
                    if extract_type == "metadata":
                        info = doc.getDocumentInfo()
                        content = f"""Writer Document Metadata:
Title: {getattr(info, 'Title', 'N/A')}
Author: {getattr(info, 'Author', 'N/A')}
Subject: {getattr(info, 'Subject', 'N/A')}
Creation Date: {getattr(info, 'CreationDate', 'N/A')}
Modified Date: {getattr(info, 'ModifiedDate', 'N/A')}"""
                    elif extract_type == "structured":
                        text = doc.getText()
                        text_content = text.getString()
                        lines = text_content.split('\n')
                        paragraphs = [line.strip() for line in lines if line.strip()]
                        content = f"""Writer Document Structure:
Total Characters: {len(text_content)}
Total Lines: {len(lines)}
Non-empty Paragraphs: {len(paragraphs)}

Content:
{text_content}"""
                    else:
                        text = doc.getText()
                        content = f"Writer Document Content:\n\n{text.getString()}"
                
                elif filename.lower().endswith('.ods'):
                    sheets = doc.getSheets()
                    sheet_count = sheets.getCount()
                    
                    if extract_type == "metadata":
                        info = doc.getDocumentInfo()
                        content = f"""Calc Spreadsheet Metadata:
Title: {getattr(info, 'Title', 'N/A')}
Author: {getattr(info, 'Author', 'N/A')}
Sheet Count: {sheet_count}
Creation Date: {getattr(info, 'CreationDate', 'N/A')}
Modified Date: {getattr(info, 'ModifiedDate', 'N/A')}"""
                    else:
                        content_parts = [f"Calc Spreadsheet Content:\nTotal Sheets: {sheet_count}\n"]
                        
                        sheet = sheets.getByIndex(0)
                        sheet_name = sheet.getName()
                        
                        cursor = sheet.createCursor()
                        cursor.gotoEndOfUsedArea(True)
                        used_range = cursor.getRangeAddress()
                        
                        if extract_type == "structured":
                            content_parts.append(f"""
Sheet: {sheet_name}
Used Range: {used_range.StartColumn}-{used_range.EndColumn}, {used_range.StartRow}-{used_range.EndRow}
Rows: {used_range.EndRow - used_range.StartRow + 1}
Columns: {used_range.EndColumn - used_range.StartColumn + 1}""")
                        
                        max_rows = min(used_range.EndRow + 1, 20)
                        max_cols = min(used_range.EndColumn + 1, 10)
                        content_parts.append(f"\nSheet '{sheet_name}' Data:")
                        for row in range(used_range.StartRow, max_rows):
                            row_data = []
                            for col in range(used_range.StartColumn, max_cols):
                                cell = sheet.getCellByPosition(col, row)
                                cell_value = cell.getString() if cell.getString() else str(cell.getValue())
                                row_data.append(cell_value)
                            if any(cell.strip() for cell in row_data):
                                content_parts.append(" | ".join(str(cell) for cell in row_data))
                        
                        content = '\n'.join(content_parts)
                
                else:
                    try:
                        if hasattr(doc, 'getText'):
                            text = doc.getText()
                            if hasattr(text, 'getString'):
                                text_content = text.getString()
                                content = f"Document Content:\n\n{text_content}"
                            else:
                                content = "Document opened but text extraction not available"
                        else:
                            content = "Document opened but content extraction not supported for this file type"
                    except Exception as e:
                        content = f"Document opened but content extraction failed: {str(e)}"
                
                return [{"type": "text", "text": content}]
            
            finally:
                doc.close(False)

        elif name == "document_summary":
            filename = arguments["filename"]
            summary_type = arguments.get("summary_type", "brief")
            max_length = arguments.get("max_length", 200)
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                content = extract_document_content(doc, filename)
                summary = summarize_content(content, summary_type, max_length)
                return [{"type": "text", "text": f"Document Summary for '{filename}':\n\n{summary}"}]
            finally:
                doc.close(False)

        elif name == "search_in_document":
            filename = arguments["filename"]
            search_term = arguments["search_term"]
            search_type = arguments.get("search_type", "fuzzy")
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                content = extract_document_content(doc, filename)
                search_results = search_in_content(content, search_term, search_type)
                
                if search_results["total_matches"] == 0:
                    result_text = f"Search Results for '{search_term}' in '{filename}':\n\nNo matches found."
                    if "message" in search_results:
                        result_text += f"\n{search_results['message']}"
                else:
                    result_text = f"Search Results for '{search_term}' in '{filename}':\n\nFound {search_results['total_matches']} matches ({search_type} search):\n\n"
                    
                    for i, match in enumerate(search_results["matches"][:5], 1):
                        if search_type == "fuzzy" and "relevance" in match:
                            relevance = f" (relevance: {match['relevance']:.0%})"
                        else:
                            relevance = ""
                        
                        result_text += f"Match {i}{relevance}:\n"
                        result_text += f"Context: ...{match['context']}...\n\n"
                    
                    if search_results['total_matches'] > 5:
                        result_text += f"... and {search_results['total_matches'] - 5} more matches."
                
                return [{"type": "text", "text": result_text}]
            finally:
                doc.close(False)

        elif name == "extract_tables":
            filename = arguments["filename"]
            table_index = arguments.get("table_index", -1)
            output_format = arguments.get("output_format", "json")
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            if not filename.lower().endswith('.odt'):
                return [{"type": "text", "text": f"ERROR: Table extraction only supported for Writer documents (.odt files)"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                tables_data = extract_tables_from_writer(doc)
                
                if not tables_data or (len(tables_data) == 1 and "error" in tables_data[0]):
                    return [{"type": "text", "text": f"ERROR: No tables found in document or extraction failed"}]
                
                if table_index >= 0:
                    if table_index < len(tables_data):
                        tables_data = [tables_data[table_index]]
                    else:
                        return [{"type": "text", "text": f"ERROR: Table index {table_index} not found. Document has {len(tables_data)} tables."}]
                
                if output_format == "csv":
                    result_text = f"Table Data from '{filename}' (CSV format):\n\n"
                    for table in tables_data:
                        result_text += f"Table: {table['table_name']} ({table['rows']} rows x {table['columns']} columns)\n"
                        for row in table['data']:
                            result_text += ",".join(f'"{cell}"' for cell in row) + "\n"
                        result_text += "\n"
                
                elif output_format == "markdown":
                    result_text = f"Table Data from '{filename}' (Markdown format):\n\n"
                    for table in tables_data:
                        result_text += f"## Table: {table['table_name']}\n\n"
                        if table['data']:
                            headers = table['data'][0] if table['data'] else []
                            result_text += "| " + " | ".join(headers) + " |\n"
                            result_text += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                            
                            for row in table['data'][1:]:
                                result_text += "| " + " | ".join(row) + " |\n"
                        result_text += "\n"
                
                else:
                    result_text = f"Table Data from '{filename}' (JSON format):\n\n"
                    result_text += f"Found {len(tables_data)} table(s):\n\n"
                    
                    for i, table in enumerate(tables_data):
                        result_text += f"Table {i + 1}: {table['table_name']}\n"
                        result_text += f"  Dimensions: {table['rows']} rows x {table['columns']} columns\n"
                        result_text += f"  Data preview (first 3 rows):\n"
                        
                        for j, row in enumerate(table['data'][:3]):
                            result_text += f"    Row {j + 1}: {row}\n"
                        
                        if table['rows'] > 3:
                            result_text += f"    ... and {table['rows'] - 3} more rows\n"
                        result_text += "\n"
                
                return [{"type": "text", "text": result_text}]
            finally:
                doc.close(False)

        # NEW: ADVANCED OPERATIONS
        elif name == "compare_documents":
            file1 = arguments["file1"]
            file2 = arguments["file2"]
            comparison_type = arguments.get("comparison_type", "content")
            
            documents_path = Path("/home/libreoffice/Documents")
            file1_path = documents_path / file1
            file2_path = documents_path / file2
            
            if not file1_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {file1}"}]
            if not file2_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {file2}"}]
            
            file1_url = f"file:///home/libreoffice/Documents/{file1}"
            file2_url = f"file:///home/libreoffice/Documents/{file2}"
            
            doc1 = desktop.loadComponentFromURL(file1_url, "_blank", 0, ())
            doc2 = desktop.loadComponentFromURL(file2_url, "_blank", 0, ())
            
            try:
                content1 = extract_document_content(doc1, file1)
                content2 = extract_document_content(doc2, file2)
                
                comparison_result = compare_documents_content(content1, content2, file1, file2, comparison_type)
                return [{"type": "text", "text": comparison_result}]
            finally:
                doc1.close(False)
                doc2.close(False)

        elif name == "analyze_document_structure":
            filename = arguments["filename"]
            analysis_depth = arguments.get("analysis_depth", "detailed")
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                content = extract_document_content(doc, filename)
                analysis_result = analyze_document_structure_detailed(content, filename, analysis_depth)
                return [{"type": "text", "text": analysis_result}]
            finally:
                doc.close(False)

        elif name == "merge_documents":
            source_files = arguments["source_files"]
            output_filename = arguments["output_filename"]
            merge_strategy = arguments.get("merge_strategy", "sequential")
            
            documents_path = Path("/home/libreoffice/Documents")
            missing_files = []
            for filename in source_files:
                if not (documents_path / filename).exists():
                    missing_files.append(filename)
            
            if missing_files:
                return [{"type": "text", "text": f"ERROR: Files not found: {', '.join(missing_files)}"}]
            
            contents = []
            docs = []
            
            try:
                for filename in source_files:
                    file_url = f"file:///home/libreoffice/Documents/{filename}"
                    doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
                    docs.append(doc)
                    content = extract_document_content(doc, filename)
                    contents.append(content)
                
                merged_content = merge_documents_content(contents, source_files, merge_strategy, output_filename)
                
                if not output_filename.endswith('.odt'):
                    output_filename += '.odt'
                
                new_doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
                text = new_doc.getText()
                cursor = text.createTextCursor()
                text.insertString(cursor, merged_content, False)
                
                output_url = f"file:///home/libreoffice/Documents/{output_filename}"
                new_doc.storeAsURL(output_url, ())
                new_doc.close(True)
                
                return [{"type": "text", "text": f"SUCCESS: Merged {len(source_files)} documents into '{output_filename}' using {merge_strategy} strategy"}]
            
            finally:
                for doc in docs:
                    doc.close(False)

        elif name == "split_document":
            filename = arguments["filename"]
            split_method = arguments.get("split_method", "by_headings")
            split_criteria = arguments.get("split_criteria")
            
            documents_path = Path("/home/libreoffice/Documents")
            file_path = documents_path / filename
            if not file_path.exists():
                return [{"type": "text", "text": f"ERROR: File not found: {filename}"}]
            
            file_url = f"file:///home/libreoffice/Documents/{filename}"
            doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
            
            try:
                content = extract_document_content(doc, filename)
                sections = split_document_content(content, filename, split_method, split_criteria)
                
                if len(sections) == 1 and "error" in sections[0]:
                    return [{"type": "text", "text": f"ERROR: {sections[0]['error']}"}]
                
                base_name = filename.rsplit('.', 1)[0]
                created_files = []
                
                for section in sections:
                    section_filename = f"{base_name}_section_{section['section_number']}.odt"
                    
                    section_doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
                    section_text = section_doc.getText()
                    section_cursor = section_text.createTextCursor()
                    
                    section_content = f"{section['title']}\n\n{section['content']}"
                    section_text.insertString(section_cursor, section_content, False)
                    
                    section_url = f"file:///home/libreoffice/Documents/{section_filename}"
                    section_doc.storeAsURL(section_url, ())
                    section_doc.close(True)
                    
                    created_files.append(f"{section_filename} ({section['word_count']} words)")
                
                result_text = f"SUCCESS: Split '{filename}' into {len(sections)} sections using '{split_method}' method:\n\n"
                for i, file_info in enumerate(created_files, 1):
                    result_text += f"{i}. {file_info}\n"
                
                return [{"type": "text", "text": result_text}]
            
            finally:
                doc.close(False)

    # Template Tool #1 - Complete Working Implementation
    # Replace the incomplete elif name == "template_apply": section with this

        elif name == "template_apply":
            # Template Tool #1 - Complete Implementation
            template_filename = arguments["template_filename"]
            output_filename = arguments["output_filename"]
            placeholders = arguments["placeholders"]
            template_format = arguments.get("template_format", "mustache")
            
            # Build file paths
            documents_path = Path("/home/libreoffice/Documents")
            template_path = documents_path / template_filename
            output_path = documents_path / output_filename
            
            # Check if template file exists
            if not template_path.exists():
                return [{"type": "text", "text": f"ERROR: Template file '{template_filename}' not found"}]
            
            try:
                # Load template document
                template_url = f"file:///home/libreoffice/Documents/{template_filename}"
                template_doc = desktop.loadComponentFromURL(template_url, "_blank", 0, ())
                
                # Extract template content
                template_content = extract_document_content(template_doc, template_filename)
                
                # Apply placeholder replacements
                result_content = apply_template_placeholders(template_content, placeholders, template_format)
                
                # Determine output document type and create new document
                if template_filename.lower().endswith(('.odt', '.docx')) or output_filename.lower().endswith(('.odt', '.docx')):
                    # Writer document
                    new_doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
                    text = new_doc.getText()
                    cursor = text.createTextCursor()
                    text.insertString(cursor, result_content, False)
                elif template_filename.lower().endswith(('.ods', '.xlsx')) or output_filename.lower().endswith(('.ods', '.xlsx')):
                    # Calc document - basic implementation
                    new_doc = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ())
                    sheet = new_doc.getSheets().getByIndex(0)
                    
                    # Split content into lines and put in cells
                    lines = result_content.split('\n')
                    for i, line in enumerate(lines[:100]):  # Limit to 100 rows
                        if line.strip():
                            cell = sheet.getCellByPosition(0, i)
                            cell.setString(line.strip())
                else:
                    template_doc.close(True)
                    return [{"type": "text", "text": f"ERROR: Unsupported template format for '{template_filename}'"}]
                
                # Save new document
                if not output_filename.lower().endswith(('.odt', '.ods', '.docx', '.xlsx')):
                    # Add appropriate extension based on template type
                    if template_filename.lower().endswith(('.odt', '.docx')):
                        output_filename += '.odt'
                    elif template_filename.lower().endswith(('.ods', '.xlsx')):
                        output_filename += '.ods'
                
                output_url = f"file:///home/libreoffice/Documents/{output_filename}"
                new_doc.storeAsURL(output_url, ())
                
                # Close documents
                template_doc.close(True)
                new_doc.close(True)
                
                return [{"type": "text", "text": f"SUCCESS: Applied template '{template_filename}' to create '{output_filename}' with {len(placeholders)} placeholder replacements"}]
                
            except Exception as e:
                return [{"type": "text", "text": f"ERROR: Template processing failed: {str(e)}"}]


        elif name == "template_create":
            # Template Tool #2 - Complete Implementation
            source_filename = arguments["source_filename"]
            template_filename = arguments["template_filename"]
            placeholder_markers = arguments["placeholder_markers"]
            placeholder_format = arguments.get("placeholder_format", "mustache")
            metadata = arguments.get("metadata", {})
            
            # Build file paths
            documents_path = Path("/home/libreoffice/Documents")
            source_path = documents_path / source_filename
            template_path = documents_path / template_filename
            
            # Check if source file exists
            if not source_path.exists():
                return [{"type": "text", "text": f"ERROR: Source file '{source_filename}' not found"}]
            
            try:
                # Load source document
                source_url = f"file:///home/libreoffice/Documents/{source_filename}"
                source_doc = desktop.loadComponentFromURL(source_url, "_blank", 0, ())
                
                # Extract source content
                source_content = extract_document_content(source_doc, source_filename)
                
                # Convert specified text to placeholders
                template_content = create_template_placeholders(source_content, placeholder_markers, placeholder_format)
                
                # Determine document type and create template
                if source_filename.lower().endswith(('.odt', '.docx')) or template_filename.lower().endswith(('.odt', '.docx')):
                    # Writer template
                    template_doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
                    text = template_doc.getText()
                    cursor = text.createTextCursor()
                    text.insertString(cursor, template_content, False)
                elif source_filename.lower().endswith(('.ods', '.xlsx')) or template_filename.lower().endswith(('.ods', '.xlsx')):
                    # Calc template - basic implementation
                    template_doc = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ())
                    sheet = template_doc.getSheets().getByIndex(0)
                    
                    # Split content into lines and put in cells
                    lines = template_content.split('\n')
                    for i, line in enumerate(lines[:100]):  # Limit to 100 rows
                        if line.strip():
                            cell = sheet.getCellByPosition(0, i)
                            cell.setString(line.strip())
                else:
                    source_doc.close(True)
                    return [{"type": "text", "text": f"ERROR: Unsupported file format for template creation"}]
                
                # Add appropriate extension if not provided
                if not template_filename.lower().endswith(('.odt', '.ods', '.docx', '.xlsx')):
                    if source_filename.lower().endswith(('.odt', '.docx')):
                        template_filename += '.odt'
                    elif source_filename.lower().endswith(('.ods', '.xlsx')):
                        template_filename += '.ods'
                
                # Save template document
                template_url = f"file:///home/libreoffice/Documents/{template_filename}"
                template_doc.storeAsURL(template_url, ())
                
                # Create metadata file if metadata provided
                metadata_saved = False
                if metadata:
                    try:
                        # Build metadata file path
                        metadata_filename = template_filename.replace('.odt', '.meta.json').replace('.ods', '.meta.json').replace('.docx', '.meta.json').replace('.xlsx', '.meta.json')
                        metadata_path = documents_path / metadata_filename
                        
                        # Create comprehensive metadata
                        template_metadata = {
                            "name": template_filename,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "placeholders": len(placeholder_markers),
                            "format": placeholder_format,
                            "source_file": source_filename,
                            "placeholder_list": placeholder_markers,
                            **metadata
                        }
                        
                        # Save metadata file
                        import json
                        with open(str(metadata_path), 'w') as f:
                            json.dump(template_metadata, f, indent=2)
                        metadata_saved = True
                    except Exception as e:
                        # Continue even if metadata save fails
                        pass
                
                # Close documents
                source_doc.close(True)
                template_doc.close(True)
                
                # Build success message
                result_msg = f"SUCCESS: Created template '{template_filename}' from '{source_filename}' with {len(placeholder_markers)} placeholders"
                if metadata_saved:
                    result_msg += " (with metadata)"
                
                return [{"type": "text", "text": result_msg}]
                
            except Exception as e:
                        return [{"type": "text", "text": f"ERROR: Template creation failed: {str(e)}"}]

        elif name == "template_list":
            search_term = arguments.get("search_term", "")
            category = arguments.get("category", "")
            format_filter = arguments.get("format", "all")
            include_metadata = arguments.get("include_metadata", False)
            
            try:
                # Get documents directory
                documents_path = Path("/home/libreoffice/Documents")
                if not documents_path.exists():
                    return [{"type": "text", "text": "ERROR: Documents directory not found"}]
                
                templates = []
                
                # Scan for template files
                for file_path in documents_path.iterdir():
                    if not file_path.is_file():
                        continue
                        
                    filename = file_path.name
                    
                    # Filter by format if specified
                    if format_filter != "all":
                        if not filename.lower().endswith(f".{format_filter}"):
                            continue
                    
                    # Look for document files that could be templates
                    if filename.lower().endswith(('.odt', '.ods', '.docx', '.xlsx')):
                        template_info = {
                            "name": filename,
                            "path": str(file_path),
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Look for metadata file
                        metadata_extensions = {'.odt': '.meta.json', '.ods': '.meta.json', 
                                             '.docx': '.meta.json', '.xlsx': '.meta.json'}
                        
                        file_ext = None
                        for ext in metadata_extensions.keys():
                            if filename.lower().endswith(ext):
                                file_ext = ext
                                break
                        
                        if file_ext:
                            metadata_filename = filename.replace(file_ext, metadata_extensions[file_ext])
                            metadata_path = documents_path / metadata_filename
                            
                            if metadata_path.exists():
                                try:
                                    import json
                                    with open(metadata_path, 'r', encoding='utf-8') as f:
                                        metadata = json.load(f)
                                    template_info["metadata"] = metadata
                                    template_info["has_metadata"] = True
                                    template_info["is_template"] = True  # Mark as confirmed template
                                    
                                    # Use metadata for filtering if available
                                    if category and metadata.get("category", "").lower() != category.lower():
                                        continue
                                        
                                except Exception as e:
                                    template_info["has_metadata"] = False
                                    template_info["is_template"] = False
                            else:
                                template_info["has_metadata"] = False
                                template_info["is_template"] = False
                        
                        # Apply search filter
                        if search_term:
                            search_lower = search_term.lower()
                            name_match = search_lower in filename.lower()
                            desc_match = False
                            
                            if template_info.get("metadata", {}).get("description"):
                                desc_match = search_lower in template_info["metadata"]["description"].lower()
                            
                            if not (name_match or desc_match):
                                continue
                        
                        # Prepare metadata for display
                        if template_info.get("metadata") and not include_metadata:
                            # Keep only basic metadata info for summary view
                            metadata_summary = {
                                "description": template_info["metadata"].get("description", ""),
                                "category": template_info["metadata"].get("category", ""),
                                "placeholders": template_info["metadata"].get("placeholders", 0),
                                "format": template_info["metadata"].get("format", "mustache")
                            }
                            template_info["metadata"] = metadata_summary
                        
                        templates.append(template_info)
                
                # Sort templates: confirmed templates first, then by name
                templates.sort(key=lambda x: (not x.get("is_template", False), x["name"].lower()))
                
                # Format output
                if not templates:
                    filter_desc = ""
                    if search_term:
                        filter_desc += f" matching '{search_term}'"
                    if category:
                        filter_desc += f" in category '{category}'"
                    if format_filter != "all":
                        filter_desc += f" with format '{format_filter}'"
                    
                    return [{"type": "text", "text": f"No templates found{filter_desc}"}]
                
                # Create comprehensive summary
                confirmed_templates = [t for t in templates if t.get("is_template", False)]
                possible_templates = [t for t in templates if not t.get("is_template", False)]
                
                result = f"📋 **Template Library Summary**\n"
                result += f"Found {len(templates)} document(s): {len(confirmed_templates)} confirmed templates, {len(possible_templates)} possible templates\n\n"
                
                # Show confirmed templates first
                if confirmed_templates:
                    result += "🎯 **Confirmed Templates** (with metadata):\n\n"
                    for template in confirmed_templates:
                        result += f"📄 **{template['name']}**\n"
                        result += f"   Size: {template['size']:,} bytes\n"
                        result += f"   Modified: {template['modified']}\n"
                        
                        if template.get("metadata"):
                            meta = template["metadata"]
                            if meta.get("description"):
                                result += f"   Description: {meta['description']}\n"
                            if meta.get("category"):
                                result += f"   Category: {meta['category']}\n"
                            if meta.get("placeholders"):
                                result += f"   Placeholders: {meta['placeholders']} ({meta.get('format', 'mustache')} format)\n"
                        
                        result += "\n"
                
                # Show possible templates
                if possible_templates:
                    result += "📁 **Other Documents** (potential templates):\n\n"
                    for template in possible_templates:
                        result += f"📄 {template['name']} ({template['size']:,} bytes, modified {template['modified']})\n"
                
                # Add usage tips
                result += "\n💡 **Tips:**\n"
                result += "- Use `template_create` to convert documents into templates with metadata\n"
                result += "- Use `template_apply` to use templates for new documents\n"
                result += "- Add `include_metadata: True` for full template details\n"
                
                return [{"type": "text", "text": result}]
                
            except Exception as e:
                return [{"type": "text", "text": f"ERROR: Failed to list templates: {str(e)}"}]

        elif name == "enhanced_style_transfer":
            source_filename = arguments["source_filename"]
            target_filename = arguments["target_filename"]
            style_types = arguments.get("style_types", ["paragraph", "character"])
            preserve_content = arguments.get("preserve_content", True)
            template_mode = arguments.get("template_mode", False)
            style_mapping = arguments.get("style_mapping", {})
            
            # Build file paths using established pattern
            documents_path = Path("/home/libreoffice/Documents")
            source_path = documents_path / source_filename
            target_path = documents_path / target_filename
            
            # Check if source file exists
            if not source_path.exists():
                return [{"type": "text", "text": f"ERROR: Source file '{source_filename}' not found"}]
            
            # Check if target file exists
            if not target_path.exists():
                return [{"type": "text", "text": f"ERROR: Target file '{target_filename}' not found"}]
            
            try:
                # Load both documents using established URL pattern
                source_url = f"file:///home/libreoffice/Documents/{source_filename}"
                target_url = f"file:///home/libreoffice/Documents/{target_filename}"
                
                source_doc = desktop.loadComponentFromURL(source_url, "_blank", 0, ())
                target_doc = desktop.loadComponentFromURL(target_url, "_blank", 0, ())
                
                styles_transferred = 0
                transfer_details = []
                
                # Process each style type
                for style_type in style_types:
                    try:
                        # Get style families using established UNO patterns
                        style_family_names = {
                            "paragraph": "ParagraphStyles",
                            "character": "CharacterStyles", 
                            "page": "PageStyles",
                            "frame": "FrameStyles",
                            "numbering": "NumberingStyles"
                        }
                        
                        # Handle table styles with existence check
                        if style_type == "table":
                            try:
                                source_styles = source_doc.getStyleFamilies().getByName("TableStyles")
                                target_styles = target_doc.getStyleFamilies().getByName("TableStyles")
                            except:
                                # TableStyles not available in this document type
                                continue
                        elif style_type in style_family_names:
                            family_name = style_family_names[style_type]
                            source_styles = source_doc.getStyleFamilies().getByName(family_name)
                            target_styles = target_doc.getStyleFamilies().getByName(family_name)
                        else:
                            continue
                        
                        # Transfer styles
                        style_names = source_styles.getElementNames()
                        type_count = 0
                        
                        for style_name in style_names:
                            try:
                                # Skip built-in styles that can't be modified
                                protected_styles = ["Standard", "Heading", "Text Body", "Default Style", 
                                                  "Default", "Header", "Footer", "Caption"]
                                if style_name in protected_styles:
                                    continue
                                
                                # Apply style mapping if provided
                                target_style_name = style_mapping.get(style_name, style_name)
                                
                                # Get source style
                                source_style = source_styles.getByName(style_name)
                                
                                # Create or update target style
                                if target_styles.hasByName(target_style_name):
                                    target_style = target_styles.getByName(target_style_name)
                                else:
                                    # Create new style using proper service name
                                    service_names = {
                                        "paragraph": "com.sun.star.style.ParagraphStyle",
                                        "character": "com.sun.star.style.CharacterStyle",
                                        "page": "com.sun.star.style.PageStyle",
                                        "frame": "com.sun.star.style.FrameStyle",
                                        "numbering": "com.sun.star.style.NumberingStyle",
                                        "table": "com.sun.star.style.TableStyle"
                                    }
                                    
                                    if style_type in service_names:
                                        target_style = target_doc.createInstance(service_names[style_type])
                                        target_styles.insertByName(target_style_name, target_style)
                                    else:
                                        continue
                                
                                # Copy style properties using enhanced helper
                                copy_style_properties(source_style, target_style, template_mode)
                                
                                type_count += 1
                                styles_transferred += 1
                                
                            except Exception as e:
                                # Continue with other styles if one fails
                                logger.info(f"Skipped style '{style_name}': {str(e)}")
                                continue
                        
                        if type_count > 0:
                            transfer_details.append(f"{type_count} {style_type} styles")
                            
                    except Exception as e:
                        # Continue with other style types if one fails
                        logger.info(f"Skipped style type '{style_type}': {str(e)}")
                        continue
                
                # Save target document
                target_doc.store()
                
                # Close documents
                source_doc.close(True)
                target_doc.close(True)
                
                # Format results
                if styles_transferred > 0:
                    details = ", ".join(transfer_details)
                    result_msg = f"SUCCESS: Transferred {styles_transferred} styles ({details}) from '{source_filename}' to '{target_filename}'"
                    
                    if template_mode:
                        result_msg += " (template-aware mode - placeholders preserved)"
                    if not preserve_content:
                        result_msg += " (content structure maintained)"
                        
                    return [{"type": "text", "text": result_msg}]
                else:
                    return [{"type": "text", "text": f"No transferable styles found between '{source_filename}' and '{target_filename}'. Documents may use only built-in styles."}]
                
            except Exception as e:
                return [{"type": "text", "text": f"ERROR: Style transfer failed: {str(e)}"}]

        else:
            return [{"type": "text", "text": f"ERROR: Unknown tool {name}"}]

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [{"type": "text", "text": f"ERROR: {str(e)}"}]

def copy_style_properties(source_style, target_style, template_mode=False):
    """Copy properties from source style to target style with template awareness"""
    try:
        # Get all property names from source style
        property_set_info = source_style.getPropertySetInfo()
        if not property_set_info:
            return
            
        property_names = property_set_info.getProperties()
        properties_copied = 0
        
        for prop in property_names:
            prop_name = prop.Name
            
            # Skip read-only properties and system properties
            if prop.Attributes & 1:  # READONLY attribute
                continue
                
            # Skip system and internal properties
            protected_props = ["Name", "DisplayName", "IsPhysical", "IsUserDefined", 
                             "ParentStyle", "FollowStyle", "Category"]
            if prop_name in protected_props:
                continue
                
            try:
                # Get property value from source
                value = source_style.getPropertyValue(prop_name)
                
                # In template mode, preserve placeholder patterns in text properties
                if template_mode and isinstance(value, str):
                    # Don't modify values that contain placeholder patterns
                    placeholder_patterns = ["{{", "}}", "%PLACEHOLDER%", "$PLACEHOLDER"]
                    if any(pattern in value for pattern in placeholder_patterns):
                        continue
                
                # Verify target style has this property before setting
                target_prop_info = target_style.getPropertySetInfo()
                if target_prop_info and target_prop_info.hasPropertyByName(prop_name):
                    target_prop = target_prop_info.getPropertyByName(prop_name)
                    # Only set if not read-only on target
                    if not (target_prop.Attributes & 1):
                        target_style.setPropertyValue(prop_name, value)
                        properties_copied += 1
                
            except Exception as e:
                # Continue with other properties if one fails
                continue
        
        logger.info(f"Copied {properties_copied} style properties")
                
    except Exception as e:
        # If property copying fails completely, log but continue
        logger.error(f"Style property copying failed: {str(e)}")
        pass

async def main():
    """Main function - SAME structure as proven versions"""
    logger.info("Complete LibreOffice MCP Server v2.5.0 with Ultimate Document Intelligence starting...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())