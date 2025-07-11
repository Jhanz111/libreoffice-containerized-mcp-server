# LibreOffice MCP Server API Documentation

## 🔧 Complete Tool Reference Guide

This document provides comprehensive documentation for all 15 tools available in the LibreOffice MCP Server v2.5.2.

## 📝 Document Creation Tools

### `create_writer_document`

Create a new LibreOffice Writer document with specified content.

**Parameters:**

- `content` (string, required): The text content for the document
- `filename` (string, required): Name for the new document (without extension)

**Example:**

```
Create a business proposal document with executive summary and project timeline
```

**Response:** Success message with created filename (.odt)

### `create_calc_spreadsheet`

Create a new LibreOffice Calc spreadsheet with data and formatting.

**Parameters:**

- `filename` (string, required): Name for the new spreadsheet
- `data` (array, optional): 2D array of cell data
- `headers` (array, optional): Column headers
- `formatting` (object, optional): Cell formatting options

**Example:**

```
Create a budget spreadsheet with monthly expenses and income tracking
```

**Response:** Success message with created filename (.ods)

### `convert_document`

Convert documents between different formats.

**Parameters:**

- `source_filename` (string, required): Source document name
- `target_format` (string, required): Target format (pdf, docx, xlsx, etc.)
- `output_filename` (string, optional): Custom output name

**Supported Formats:**

- **Input**: odt, ods, odp, doc, docx, xls, xlsx, ppt, pptx
- **Output**: pdf, odt, ods, docx, xlsx, html, txt

**Example:**

```
Convert my quarterly report from ODT to PDF format
```

**Response:** Success message with converted filename

## 📖 Document Intelligence Tools

### `read_document`

Extract and analyze content from existing documents.

**Parameters:**

- `filename` (string, required): Document to read
- `extract_metadata` (boolean, optional): Include document metadata
- `extract_formatting` (boolean, optional): Include formatting information

**Example:**

```
Read the contents of my meeting notes document
```

**Response:** Document content, metadata, and structure information

### `document_summary`

Generate AI-powered summaries of document content.

**Parameters:**

- `filename` (string, required): Document to summarize
- `summary_length` (string, optional): "brief", "detailed", or "comprehensive"
- `focus_areas` (array, optional): Specific topics to emphasize

**Example:**

```
Create a comprehensive summary of the annual report focusing on financial performance
```

**Response:** Structured summary with key points and insights

### `search_in_document`

Find specific content within documents using advanced search.

**Parameters:**

- `filename` (string, required): Document to search
- `search_term` (string, required): Text to find
- `case_sensitive` (boolean, optional): Case-sensitive search
- `whole_words` (boolean, optional): Match whole words only
- `include_context` (boolean, optional): Include surrounding text

**Example:**

```
Search for "budget allocation" in the strategic plan document
```

**Response:** Search results with locations and context

### `extract_tables`

Extract structured data from tables within documents.

**Parameters:**

- `filename` (string, required): Document containing tables
- `table_index` (number, optional): Specific table to extract (0-based)
- `include_headers` (boolean, optional): Include table headers
- `output_format` (string, optional): "json", "csv", or "array"

**Example:**

```
Extract all financial tables from the quarterly report
```

**Response:** Structured table data in specified format

## 🔄 Advanced Operations Tools

### `compare_documents`

Intelligent comparison between two documents.

**Parameters:**

- `document1` (string, required): First document to compare
- `document2` (string, required): Second document to compare
- `comparison_type` (string, optional): "content", "structure", or "both"
- `highlight_changes` (boolean, optional): Create highlighted difference document

**Example:**

```
Compare the old and new contract versions and highlight all changes
```

**Response:** Detailed comparison report with differences identified

### `analyze_document_structure`

Deep structural analysis of document organization.

**Parameters:**

- `filename` (string, required): Document to analyze
- `include_styles` (boolean, optional): Analyze style usage
- `include_hierarchy` (boolean, optional): Map heading structure
- `include_references` (boolean, optional): Find cross-references

**Example:**

```
Analyze the structure of my thesis document including heading hierarchy
```

**Response:** Comprehensive structural analysis and recommendations

### `merge_documents`

Intelligently combine multiple documents into one.

**Parameters:**

- `source_files` (array, required): List of documents to merge
- `output_filename` (string, required): Name for merged document
- `merge_strategy` (string, optional): "sequential", "by_section", or "custom"
- `preserve_formatting` (boolean, optional): Maintain original formatting

**Example:**

```
Merge all quarterly reports into a single annual summary document
```

**Response:** Success message with merged document details

### `split_document`

Break documents into logical sections or separate files.

**Parameters:**

- `source_filename` (string, required): Document to split
- `split_criteria` (string, required): "by_heading", "by_page", or "by_section"
- `output_prefix` (string, optional): Prefix for generated files
- `preserve_styles` (boolean, optional): Maintain formatting in splits

**Example:**

```
Split the manual by chapters, creating separate documents for each section
```

**Response:** List of created documents with split details

## 🌟 Revolutionary Template System Tools

### `template_create`

Convert existing documents into reusable templates with placeholders.

**Parameters:**

- `source_filename` (string, required): Document to convert to template
- `template_filename` (string, required): Name for the new template
- `placeholder_markers` (array, required): Text strings to convert to placeholders
- `placeholder_format` (string, optional): "mustache" ({{}}), "percent" (%%), or "dollar" ($$)
- `metadata` (object, optional): Template description and categorization

**Placeholder Formats:**

- **Mustache**: `{{placeholder_name}}` (default)
- **Percent**: `%placeholder_name%`
- **Dollar**: `$placeholder_name$`

**Example:**

```
Create a template from my invoice document with placeholders for client_name, amount, and due_date
```

**Response:** Success message with template details and placeholder count

### `template_apply`

Apply templates to generate new documents with dynamic content.

**Parameters:**

- `template_filename` (string, required): Template to use
- `output_filename` (string, required): Name for generated document
- `placeholders` (object, required): Key-value pairs for placeholder replacement
- `template_format` (string, optional): Format of placeholders in template

**Example:**

```
Apply the invoice template with client_name="ABC Corp", amount="$5,000", due_date="January 15, 2025"
```

**Response:** Success message with generated document details

### `template_list`

Browse and discover available templates with advanced filtering.

**Parameters:**

- `search_term` (string, optional): Filter templates by name or description
- `category` (string, optional): Filter by template category
- `format` (string, optional): Filter by file format ("odt", "ods", "all")
- `include_metadata` (boolean, optional): Include detailed template information

**Example:**

```
Show me all business templates with their descriptions and placeholder information
```

**Response:** Formatted list of templates with metadata and usage information

### `enhanced_style_transfer`

Professional style transfer between documents with template awareness.

**Parameters:**

- `source_filename` (string, required): Document with styles to copy
- `target_filename` (string, required): Document to apply styles to
- `style_types` (array, optional): Types to transfer ("paragraph", "character", "page", "frame", "numbering", "table")
- `preserve_content` (boolean, optional): Keep existing content
- `template_mode` (boolean, optional): Preserve placeholders during transfer
- `style_mapping` (object, optional): Map source styles to target style names

**Style Types:**

- **paragraph**: Text paragraph styles
- **character**: Character formatting styles
- **page**: Page layout and formatting
- **frame**: Frame and text box styles
- **numbering**: List and numbering styles
- **table**: Table formatting styles

**Example:**

```
Transfer formatting from the brand guide to my presentation, preserving all template placeholders
```

**Response:** Success message with transferred style count and details

## 📊 Response Formats

### Success Responses

All successful operations return structured responses with:

- **Status**: "SUCCESS" indicator
- **Details**: Operation-specific information
- **Metadata**: File information (size, format, creation time)
- **Performance**: Execution time for monitoring

### Error Responses

Error responses include:

- **Error Type**: Category of error (file, format, processing)
- **Description**: Human-readable error message
- **Suggestions**: Recommended solutions
- **Context**: Relevant operation details

## ⚡ Performance Characteristics

### Operation Speed Benchmarks

|Operation Type|Expected Time|Notes|
|---|---|---|
|Document Creation|2-5 seconds|Basic documents|
|Document Reading|1-3 seconds|10-page average|
|Template Operations|3-7 seconds|With placeholders|
|Style Transfer|5-10 seconds|Multiple style types|
|Complex Analysis|8-15 seconds|Large documents|

### Optimization Tips

- **Large Documents**: Use specific tools rather than full document operations
- **Template Performance**: Pre-create templates for frequently used formats
- **Style Transfer**: Limit style types to necessary categories
- **Batch Operations**: Process multiple small operations rather than single large ones

## 🔧 Advanced Usage Patterns

### Template Workflow Pattern

1. **Create Template**: Convert document → template with placeholders
2. **Apply Template**: Generate documents → with dynamic content
3. **Manage Library**: Browse and organize → template collection
4. **Style Enhancement**: Transfer formatting → while preserving placeholders

### Document Intelligence Pattern

1. **Read Document**: Extract content → and metadata
2. **Analyze Structure**: Understand organization → and hierarchy
3. **Search Content**: Find specific information → with context
4. **Extract Data**: Pull structured information → for processing

### Document Processing Pattern

1. **Compare Documents**: Identify differences → and changes
2. **Merge Content**: Combine information → intelligently
3. **Split Documents**: Organize content → into logical sections
4. **Convert Formats**: Transform documents → for different uses

## 🛠️ Integration Examples

### Workflow Automation

```python
# Example: Automated report generation
1. Read source data documents
2. Create report template with placeholders
3. Apply template with current data
4. Transfer professional styling
5. Convert to PDF for distribution
```

### Template Library Management

```python
# Example: Template ecosystem
1. Create templates from existing documents
2. Organize templates by category
3. Search templates for specific use cases
4. Apply templates with dynamic content
5. Maintain consistent styling across documents
```

## 📚 Additional Resources

- [Installation Guide](https://claude.ai/chat/INSTALLATION.md)
- [Troubleshooting Guide](https://claude.ai/chat/Troubleshooting-Guide.md)
- [Usage Examples](https://claude.ai/chat/examples/)
- [Container Configuration](https://claude.ai/chat/Image-Build-Files/)

---

**📚 This API enables unprecedented document automation capabilities through AI-powered LibreOffice integration!**