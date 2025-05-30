import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import {
  Container,
  Typography,
  Box,
  Paper,
  Divider,
  CircularProgress,
  Chip,
  Button,
  Avatar,
  alpha,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Checkbox,
  DialogContentText,
  Radio,
  RadioGroup,
  FormControl,
  FormLabel,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FolderIcon from '@mui/icons-material/Folder';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import StorageIcon from '@mui/icons-material/Storage';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import DataObjectIcon from '@mui/icons-material/DataObject';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import WarningIcon from '@mui/icons-material/Warning';
import CodeIcon from '@mui/icons-material/Code';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { colors } from '../App';
import PsychologyIcon from '@mui/icons-material/Psychology';

// Helper function to normalize language identifiers
const normalizeLanguage = (languageId) => {
  // Default to plaintext if no language is provided
  if (!languageId) return 'text';
  
  // Map Cursor/VSCode language IDs to Prism supported languages
  const languageMap = {
    'plaintext': 'text',
    'markdown': 'markdown',
    'javascript': 'javascript',
    'typescript': 'typescript',
    'python': 'python',
    'java': 'java',
    'csharp': 'csharp',
    'c': 'c',
    'cpp': 'cpp',
    'html': 'html',
    'css': 'css',
    'json': 'json',
    'go': 'go',
    'rust': 'rust',
    'php': 'php',
    'ruby': 'ruby',
    'swift': 'swift',
    'kotlin': 'kotlin',
    'sql': 'sql',
    'shell': 'bash',
    'bash': 'bash',
    'powershell': 'powershell',
    'yaml': 'yaml',
    'xml': 'xml',
  };
  
  // Clean up the language ID (lowercase, remove spaces, etc.)
  const normalizedId = languageId.toLowerCase().trim();
  
  // Return the mapped language or the original if not found
  return languageMap[normalizedId] || normalizedId;
};

const ChatDetail = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [chat, setChat] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [exportModalOpen, setExportModalOpen] = useState(false);
  const [formatDialogOpen, setFormatDialogOpen] = useState(false);
  const [exportFormat, setExportFormat] = useState('html');
  const [dontShowExportWarning, setDontShowExportWarning] = useState(false);

  // Custom styles for tool calls and thinking blocks
  const styles = {
    thinkingBlock: {
      backgroundColor: alpha('#2d3748', 0.6),
      borderRadius: 1,
      border: '1px solid',
      borderColor: '#4a5568',
      marginTop: 2,
      padding: 2
    },
    thinkingHeader: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: 1
    },
    thinkingLabel: {
      color: '#a0aec0',
      display: 'flex',
      alignItems: 'center',
      gap: 0.5,
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: '0.75rem',
    },
    thinkingContent: {
      whiteSpace: 'pre-wrap',
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: '0.85rem',
      overflow: 'auto',
      color: '#e2e8f0'
    },
    toolCallBlock: {
      marginTop: 2,
      borderRadius: 1,
      overflow: 'hidden',
      border: '1px solid',
      borderColor: alpha('#66b3ff', 0.3),
    },
    toolCallHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: 1.5,
      backgroundColor: alpha('#2b4562', 0.7),
      borderBottom: '1px solid',
      borderBottomColor: alpha('#66b3ff', 0.2),
      borderLeft: '4px solid',
    },
    toolName: {
      fontFamily: "'JetBrains Mono', monospace",
      fontWeight: 500,
      fontSize: '0.85rem',
      display: 'flex',
      alignItems: 'center',
      gap: 1
    },
    toolParams: {
      padding: 1.5,
      borderBottom: '1px solid',
      borderBottomColor: alpha('#66b3ff', 0.2)
    },
    toolResult: {
      padding: 1.5
    },
    toolSectionHeader: {
      color: alpha('#9cdefd', 0.7),
      fontWeight: 'medium',
      display: 'block',
      marginBottom: 1,
      fontSize: '0.75rem',
    }
  };

  useEffect(() => {
    const fetchChat = async () => {
      try {
        const response = await axios.get(`/api/chat/${sessionId}`);
        console.log('FULL CHAT RESPONSE DATA:', JSON.stringify(response.data).slice(0, 500) + '...');
        
        // Debug check for codeBlocks in messages
        if (response.data && response.data.messages) {
          console.log('Messages count:', response.data.messages.length);
          response.data.messages.forEach((msg, i) => {
            console.log(`Message ${i} - has codeBlocks:`, !!msg.codeBlocks, 
              msg.codeBlocks ? `(${msg.codeBlocks.length})` : '');
            if (msg.codeBlocks && msg.codeBlocks.length > 0) {
              console.log(`Message ${i} - first codeBlock:`, JSON.stringify(msg.codeBlocks[0]));
            }
          });
        }
        
        setChat(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching chat:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchChat();
    
    // Check if user has previously chosen to not show the export warning
    const warningPreference = document.cookie
      .split('; ')
      .find(row => row.startsWith('dontShowExportWarning='));
    
    if (warningPreference) {
      setDontShowExportWarning(warningPreference.split('=')[1] === 'true');
    }
  }, [sessionId]);

  // Add a useEffect hook to check for code blocks after the component renders
  useEffect(() => {
    if (chat && Array.isArray(chat.messages)) {
      // Count code blocks in all messages
      let codeBlockCount = 0;
      const messagesWithCodeBlocks = chat.messages.filter(msg => 
        msg.codeBlocks && Array.isArray(msg.codeBlocks) && msg.codeBlocks.length > 0
      );
      
      messagesWithCodeBlocks.forEach(msg => {
        codeBlockCount += msg.codeBlocks.length;
      });
      
      console.log(`RENDER CHECK: Found ${messagesWithCodeBlocks.length} messages with code blocks (${codeBlockCount} total blocks)`);
      
      // Log some details about the first code block for debugging
      if (messagesWithCodeBlocks.length > 0 && messagesWithCodeBlocks[0].codeBlocks.length > 0) {
        const firstBlock = messagesWithCodeBlocks[0].codeBlocks[0];
        console.log(`First code block language: "${firstBlock.language || 'none'}"`);
        console.log(`First code block content starts with: "${firstBlock.content.substring(0, 50)}..."`);
      }
    }
  }, [chat]);

  // Handle format dialog selection
  const handleFormatDialogOpen = () => {
    setFormatDialogOpen(true);
  };

  const handleFormatDialogClose = (confirmed) => {
    setFormatDialogOpen(false);
    
    if (confirmed) {
      // After format selection, show warning dialog or proceed directly
      if (dontShowExportWarning) {
        proceedWithExport(exportFormat);
      } else {
        setExportModalOpen(true);
      }
    }
  };

  // Handle export warning confirmation
  const handleExportWarningClose = (confirmed) => {
    setExportModalOpen(false);
    
    // Save preference in cookies if "Don't show again" is checked
    if (dontShowExportWarning) {
      const expiryDate = new Date();
      expiryDate.setFullYear(expiryDate.getFullYear() + 1); // Cookie lasts 1 year
      document.cookie = `dontShowExportWarning=true; expires=${expiryDate.toUTCString()}; path=/`;
    }
    
    // If confirmed, proceed with export
    if (confirmed) {
      proceedWithExport(exportFormat);
    }
  };

  // Function to initiate export process
  const handleExport = () => {
    // First open format selection dialog
    handleFormatDialogOpen();
  };

  // Function to actually perform the export
  const proceedWithExport = async (format) => {
    try {
      // Request the exported chat as a raw Blob so we can download it directly
      const response = await axios.get(
        `/api/chat/${sessionId}/export?format=${format}`,
        { responseType: 'blob' }
      );

      const blob = response.data;

      // Guard-check to avoid downloading an empty file
      if (!blob || blob.size === 0) {
        throw new Error('Received empty or invalid content from server');
      }

      // Ensure the blob has the correct MIME type
      const mimeType = format === 'json' ? 'application/json;charset=utf-8' : 'text/html;charset=utf-8';
      const typedBlob = blob.type ? blob : new Blob([blob], { type: mimeType });

      // Download Logic
      const extension = format === 'json' ? 'json' : 'html';
      const filename = `cursor-chat-${sessionId.slice(0, 8)}.${extension}`;
      const link = document.createElement('a');
      
      // Create an object URL for the (possibly re-typed) blob
      const url = URL.createObjectURL(typedBlob);
      link.href = url;
      link.download = filename;
      
      // Append link to the body (required for Firefox)
      document.body.appendChild(link);
      
      // Programmatically click the link to trigger the download
      link.click();
      
      // Clean up: remove the link and revoke the object URL
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export failed:', err);
      alert('Failed to export chat – check console for details');
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
        <CircularProgress sx={{ color: colors.highlightColor }} />
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Typography variant="h5" color="error">
          Error: {error}
        </Typography>
      </Container>
    );
  }

  if (!chat) {
    return (
      <Container>
        <Typography variant="h5">
          Chat not found
        </Typography>
      </Container>
    );
  }

  // Format the date safely
  let dateDisplay = 'Unknown date';
  try {
    if (chat.date) {
      const dateObj = new Date(chat.date * 1000);
      // Check if date is valid
      if (!isNaN(dateObj.getTime())) {
        dateDisplay = dateObj.toLocaleString();
      }
    }
  } catch (err) {
    console.error('Error formatting date:', err);
  }

  // Ensure messages exist
  const messages = Array.isArray(chat.messages) ? chat.messages : [];
  const projectName = chat.project?.name || 'Unknown Project';

  return (
    <Container sx={{ mb: 6 }}>
      {/* Format Selection Dialog */}
      <Dialog
        open={formatDialogOpen}
        onClose={() => handleFormatDialogClose(false)}
        aria-labelledby="format-selection-dialog-title"
      >
        <DialogTitle id="format-selection-dialog-title" sx={{ display: 'flex', alignItems: 'center' }}>
          <FileDownloadIcon sx={{ color: colors.highlightColor, mr: 1 }} />
          Export Format
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please select the export format for your chat:
          </DialogContentText>
          <FormControl component="fieldset" sx={{ mt: 2 }}>
            <RadioGroup
              aria-label="export-format"
              name="export-format"
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value)}
            >
              <FormControlLabel value="html" control={<Radio />} label="HTML" />
              <FormControlLabel value="json" control={<Radio />} label="JSON" />
            </RadioGroup>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleFormatDialogClose(false)} color="highlight">
            Cancel
          </Button>
          <Button onClick={() => handleFormatDialogClose(true)} color="highlight" variant="contained">
            Continue
          </Button>
        </DialogActions>
      </Dialog>

      {/* Export Warning Modal */}
      <Dialog
        open={exportModalOpen}
        onClose={() => handleExportWarningClose(false)}
        aria-labelledby="export-warning-dialog-title"
      >
        <DialogTitle id="export-warning-dialog-title" sx={{ display: 'flex', alignItems: 'center' }}>
          <WarningIcon sx={{ color: 'warning.main', mr: 1 }} />
          Export Warning
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please make sure your exported chat doesn't include sensitive data such as API keys and customer information.
          </DialogContentText>
          <FormControlLabel
            control={
              <Checkbox
                checked={dontShowExportWarning}
                onChange={(e) => setDontShowExportWarning(e.target.checked)}
              />
            }
            label="Don't show this warning again"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleExportWarningClose(false)} color="highlight">
            Cancel
          </Button>
          <Button onClick={() => handleExportWarningClose(true)} color="highlight" variant="contained">
            Continue Export
          </Button>
        </DialogActions>
      </Dialog>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, mt: 2 }}>
        <Button
          component={Link}
          to="/"
          startIcon={<ArrowBackIcon />}
          variant="outlined"
          sx={{ 
            borderRadius: 2,
            color: 'white'
          }}
        >
          Back to all chats
        </Button>
        
        <Button
          onClick={handleExport}
          startIcon={<FileDownloadIcon />}
          variant="contained"
          color="highlight"
          sx={{ 
            borderRadius: 2,
            position: 'relative',
            '&:hover': {
              backgroundColor: alpha(colors.highlightColor, 0.8),
            },
            '&::after': dontShowExportWarning ? null : {
              content: '""',
              position: 'absolute',
              borderRadius: '50%',
              top: '4px',
              right: '4px',
              width: '8px', // Adjusted size for button
              height: '8px' // Adjusted size for button
            },
            // Conditionally add the background color if the warning should be shown
            ...( !dontShowExportWarning && {
              '&::after': { 
                backgroundColor: 'warning.main'
              }
            })
          }}
        >
          Export
        </Button>
      </Box>

      <Paper 
        sx={{ 
          p: 0, 
          mb: 3, 
          overflow: 'hidden',
          boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
        }}
      >
        <Box sx={{ 
          background: `linear-gradient(90deg, ${colors.highlightColor} 0%, ${colors.highlightColor.light} 100%)`,
          color: 'white',
          px: 3,
          py: 1.5,
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}>
            <FolderIcon sx={{ mr: 1, fontSize: 22 }} />
            <Typography variant="h6" fontWeight="600" sx={{ mr: 1.5 }}>
              {projectName}
            </Typography>
            <Chip
              icon={<CalendarTodayIcon />}
              label={dateDisplay}
              size="small"
              sx={{ 
                fontWeight: 500,
                color: 'white',
                '& .MuiChip-icon': { color: 'white' },
                '& .MuiChip-label': { px: 1 }
              }}
            />
          </Box>
        </Box>
        
        <Box sx={{ px: 3, py: 1.5 }}>
          <Box sx={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: 2,
            alignItems: 'center'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <AccountTreeIcon sx={{ mr: 0.5, color: colors.highlightColor, opacity: 0.8, fontSize: 18 }} />
              <Typography variant="body2" color="text.secondary">
                <strong>Path:</strong> {chat.project?.rootPath || 'Unknown location'}
              </Typography>
            </Box>
            
            {chat.workspace_id && (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <StorageIcon sx={{ mr: 0.5, color: colors.highlightColor, opacity: 0.8, fontSize: 18 }} />
                <Typography variant="body2" color="text.secondary">
                  <strong>Workspace:</strong> {chat.workspace_id}
                </Typography>
              </Box>
            )}
            
            {chat.db_path && (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <DataObjectIcon sx={{ mr: 0.5, color: colors.highlightColor, opacity: 0.8, fontSize: 18 }} />
                <Typography variant="body2" color="text.secondary" sx={{ wordBreak: 'break-all' }}>
                  <strong>DB:</strong> {chat.db_path.split('/').pop()}
                </Typography>
              </Box>
            )}
          </Box>
        </Box>
      </Paper>

      <Typography variant="h5" gutterBottom fontWeight="600" sx={{ mt: 4, mb: 3 }}>
        Conversation History
      </Typography>

      {messages.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 3 }}>
          <Typography variant="body1">
            No messages found in this conversation.
          </Typography>
        </Paper>
      ) : (
        <Box sx={{ mb: 4 }}>
          {messages.map((message, index) => (
            <Box key={index} sx={{ mb: 3.5 }}>
              {/* Debug info - more explicit */}
              {console.log(`Rendering message ${index}:`)}
              {console.log(`- Role: ${message.role}`)}
              {console.log(`- Content length: ${message.content ? message.content.length : 0}`)}
              {console.log(`- codeBlocks exists: ${!!message.codeBlocks}`)}
              {console.log(`- codeBlocks is array: ${Array.isArray(message.codeBlocks)}`)}
              {console.log(`- codeBlocks length: ${message.codeBlocks && Array.isArray(message.codeBlocks) ? message.codeBlocks.length : 'N/A'}`)}
              
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                <Avatar
                  sx={{
                    bgcolor: message.role === 'user' ? colors.highlightColor : colors.secondary.main,
                    width: 32,
                    height: 32,
                    mr: 1.5,
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                  }}
                >
                  {message.role === 'user' ? <PersonIcon /> : <SmartToyIcon />}
                </Avatar>
                <Typography variant="subtitle1" fontWeight="600">
                  {message.role === 'user' ? 'You' : 'Cursor Assistant'}
                </Typography>
              </Box>
              
              <Paper 
                elevation={1}
                sx={{ 
                  p: 2.5, 
                  ml: message.role === 'user' ? 0 : 5,
                  mr: message.role === 'assistant' ? 0 : 5,
                  backgroundColor: alpha(colors.highlightColor, 0.04),
                  borderLeft: '4px solid',
                  borderColor: message.role === 'user' ? colors.highlightColor : colors.secondary.main,
                  borderRadius: 2
                }}
              >
                {/* Render regular text content */}
                {message.content && (
                  <Box sx={{ 
                    '& pre': { 
                      maxWidth: '100%', 
                      overflowX: 'auto',
                      backgroundColor: message.role === 'user' 
                        ? alpha(colors.primary.main, 0.07) 
                        : alpha(colors.highlightColor, 0.15),
                      borderRadius: 1,
                      p: 2
                    },
                    '& code': { 
                      display: 'inline-block', 
                      maxWidth: '100%', 
                      overflowX: 'auto',
                      backgroundColor: message.role === 'user' 
                        ? alpha(colors.primary.main, 0.07) 
                        : alpha(colors.highlightColor, 0.15),
                      borderRadius: 0.5,
                      px: 0.8,
                      py: 0.2,
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: '0.85rem'
                    },
                    '& img': { maxWidth: '100%' },
                    '& ul, & ol': { pl: 3 },
                    '& a': { 
                      color: message.role === 'user' ? colors.highlightColor : colors.secondary.main,
                      textDecoration: 'none',
                      '&:hover': { textDecoration: 'none' }
                    }
                  }}>
                    {typeof message.content === 'string' ? (
                      <ReactMarkdown
                        components={{
                          code({node, inline, className, children, ...props}) {
                            const match = /language-(\w+)/.exec(className || '')
                            return !inline && match ? (
                              <SyntaxHighlighter
                                language={normalizeLanguage(match[1])}
                                style={atomDark}
                                showLineNumbers={true}
                                customStyle={{
                                  margin: '0.5em 0',
                                  borderRadius: '4px',
                                  background: message.role === 'user' 
                                    ? alpha(colors.primary.main, 0.07) 
                                    : alpha(colors.highlightColor, 0.15),
                                }}
                                {...props}
                              >
                                {String(children).replace(/\n$/, '')}
                              </SyntaxHighlighter>
                            ) : (
                              <code className={className} {...props}>
                                {children}
                              </code>
                            )
                          }
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      <Typography>Content unavailable</Typography>
                    )}
                  </Box>
                )}
                
                {/* Render separate code blocks when available */}
                {message.codeBlocks && Array.isArray(message.codeBlocks) && message.codeBlocks.length > 0 && (
                  <Box sx={{ mt: message.content ? 2 : 0 }}>
                    {message.codeBlocks.map((codeBlock, blockIndex) => (
                      <Box 
                        key={blockIndex} 
                        sx={{ 
                          mt: blockIndex > 0 ? 3 : 0,
                          position: 'relative'
                        }}
                      >
                        {/* Language label */}
                        {codeBlock.language && (
                          <Chip
                            label={codeBlock.language}
                            size="small"
                            sx={{
                              position: 'absolute',
                              top: '8px',
                              right: '8px',
                              zIndex: 1,
                              backgroundColor: message.role === 'user' 
                                ? alpha(colors.primary.main, 0.1) 
                                : alpha(colors.highlightColor, 0.2),
                              color: message.role === 'user' 
                                ? colors.primary.main 
                                : colors.highlightColor,
                              fontFamily: "'JetBrains Mono', monospace",
                              fontSize: '0.7rem',
                              height: '22px'
                            }}
                          />
                        )}
                        
                        {/* Code content */}
                        <Box 
                          sx={{ 
                            borderRadius: 1,
                            overflow: 'hidden',
                            border: '1px solid',
                            borderColor: alpha(colors.highlightColor, 0.3),
                            '& pre': {
                              margin: 0,
                              fontSize: '0.85rem',
                              fontFamily: "'JetBrains Mono', monospace",
                            }
                          }}
                        >
                          <SyntaxHighlighter
                            language={normalizeLanguage(codeBlock.language || 'text')}
                            style={atomDark}
                            showLineNumbers={true}
                            customStyle={{
                              margin: 0,
                              borderRadius: 0,
                              background: message.role === 'user' 
                                ? alpha(colors.primary.main, 0.07) 
                                : alpha(colors.highlightColor, 0.15),
                              padding: '32px 16px 16px 16px', // Extra padding on top for the language label
                            }}
                          >
                            {codeBlock.content || ''}
                          </SyntaxHighlighter>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                )}
                
                {/* Display AI Thinking if available */}
                {message.thinking_html ? (
                  <Box
                    sx={{
                      mt: 2,
                      borderRadius: 1,
                      overflow: 'hidden',
                    }}
                    dangerouslySetInnerHTML={{ __html: message.thinking_html }}
                  />
                ) : message.thinking && message.thinking.text && (
                  <Box sx={styles.thinkingBlock}>
                    <Box sx={styles.thinkingHeader}>
                      <Typography 
                        variant="caption" 
                        fontWeight="medium"
                        sx={styles.thinkingLabel}
                      >
                        <PsychologyIcon fontSize="small" /> 
                        AI Thought Process
                      </Typography>
                    </Box>
                    <Typography 
                      variant="body2" 
                      component="pre"
                      sx={styles.thinkingContent}
                    >
                      {message.thinking.text}
                    </Typography>
                  </Box>
                )}
                
                {/* Display Tool Call HTML if available */}
                {message.tool_call_html ? (
                  <Box
                    sx={{
                      mt: 2,
                      borderRadius: 1,
                      overflow: 'hidden',
                    }}
                    dangerouslySetInnerHTML={{ __html: message.tool_call_html }}
                  />
                ) : message.tool_former_data && Object.keys(message.tool_former_data).length > 0 && (
                  <Box sx={styles.toolCallBlock}>
                    {/* Tool Header */}
                    <Box
                      sx={{
                        ...styles.toolCallHeader,
                        borderLeftColor: message.tool_former_data.status === 'completed' ? '#48BB78' 
                          : message.tool_former_data.status === 'error' ? '#F56565' 
                          : '#ECC94B'
                      }}
                    >
                      <Typography sx={styles.toolName}>
                        <CodeIcon fontSize="small" />
                        Called Tool: {message.tool_former_data.name || 'Unknown Tool'}
                      </Typography>
                      <Typography variant="body2">
                        {message.tool_former_data.status === 'completed' ? '✅' 
                          : message.tool_former_data.status === 'error' ? '❌' 
                          : '⏳'}
                      </Typography>
                    </Box>
                    
                    {/* Tool Parameters */}
                    {(message.tool_former_data.params || message.tool_former_data.rawArgs) && (
                      <Box sx={styles.toolParams}>
                        <Typography
                          variant="caption"
                          fontWeight="medium"
                          sx={styles.toolSectionHeader}
                        >
                          Parameters:
                        </Typography>
                        
                        <Box sx={{ maxHeight: '200px', overflow: 'auto' }}>
                          <SyntaxHighlighter
                            language="json"
                            style={atomDark}
                            customStyle={{
                              margin: 0,
                              padding: '12px',
                              borderRadius: '4px',
                              backgroundColor: alpha('#1a202c', 0.6),
                              fontSize: '0.8rem'
                            }}
                          >
                            {typeof (message.tool_former_data.params || message.tool_former_data.rawArgs) === 'string' 
                              ? (message.tool_former_data.params || message.tool_former_data.rawArgs)
                              : JSON.stringify(message.tool_former_data.params || message.tool_former_data.rawArgs, null, 2)}
                          </SyntaxHighlighter>
                        </Box>
                      </Box>
                    )}
                    
                    {/* Tool Result */}
                    {message.tool_former_data.result && (
                      <Box sx={styles.toolResult}>
                        <Typography
                          variant="caption"
                          fontWeight="medium"
                          sx={styles.toolSectionHeader}
                        >
                          Result:
                        </Typography>
                        
                        <Box sx={{ maxHeight: '200px', overflow: 'auto' }}>
                          <SyntaxHighlighter
                            language="json"
                            style={atomDark}
                            customStyle={{
                              margin: 0,
                              padding: '12px',
                              borderRadius: '4px',
                              backgroundColor: alpha('#1a202c', 0.6),
                              fontSize: '0.8rem'
                            }}
                          >
                            {typeof message.tool_former_data.result === 'string' 
                              ? message.tool_former_data.result
                              : JSON.stringify(message.tool_former_data.result, null, 2)}
                          </SyntaxHighlighter>
                        </Box>
                      </Box>
                    )}
                  </Box>
                )}
                
                {/* Show a message if no content is available */}
                {(!message.content || message.content === '') && 
                 (!message.codeBlocks || message.codeBlocks.length === 0) && 
                 (!message.thinking || !message.thinking.text) &&
                 (!message.tool_former_data || Object.keys(message.tool_former_data).length === 0) && (
                  <Typography>Content unavailable</Typography>
                )}
              </Paper>
            </Box>
          ))}
        </Box>
      )}
    </Container>
  );
};

export default ChatDetail; 