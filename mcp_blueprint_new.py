# mcp_blueprint.py
from flask import Blueprint, request, jsonify, current_app
from typing import Dict, List, TypedDict, Optional, Any, Union
from const.config import ITEMS
import uuid
import time
import logging
from datetime import datetime
from functools import wraps
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions
class SessionData(TypedDict):
    timestamp: float
    request_count: int
    last_request: float

class ContextResponse(TypedDict):
    type: str
    request_id: str
    data: Union[List[Any], Dict[str, Any]]

class ToolResponse(TypedDict):
    type: str
    request_id: str
    output: Any

class ErrorResponse(TypedDict):
    type: str
    request_id: str
    error: str
    details: Optional[str]

# Constants
SESSION_TIMEOUT = 1800  # 30 minutes
MAX_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_WINDOW = 60

# Mock data
FAQ_DATA = [
    {"id": "FAQ001", "q": "How do I track my order?", "a": "Check your order status in your account."},
    {"id": "FAQ002", "q": "What's your return policy?", "a": "30-day returns on most items."},
    {"id": "FAQ003", "q": "Shipping time?", "a": "3-5 business days standard shipping."}
]

TICKET_CATEGORIES = [
    "Order Issues",
    "Returns",
    "Product Information",
    "Technical Support",
    "Account Issues",
    "Shipping",
    "Billing",
    "General Inquiry"
]

# Active sessions storage
active_sessions: Dict[str, SessionData] = {}

# Decorator for error handling
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({
                "type": "error.response",
                "request_id": str(uuid.uuid4()),
                "error": "internal_error",
                "details": str(e)
            }), 500
    return decorated_function

# Utility functions
def validate_session(session_id: str) -> bool:
    """Validate session and check rate limits"""
    if session_id not in active_sessions:
        return False
    
    session = active_sessions[session_id]
    current_time = time.time()
    
    # Check session timeout
    if current_time - session['timestamp'] > SESSION_TIMEOUT:
        del active_sessions[session_id]
        logger.info(f"Session {session_id} expired")
        return False
    
    # Check rate limits
    if current_time - session['last_request'] < RATE_LIMIT_WINDOW:
        if session['request_count'] >= MAX_REQUESTS_PER_MINUTE:
            logger.warning(f"Rate limit exceeded for session {session_id}")
            return False
    else:
        # Reset counter for new window
        session['request_count'] = 0
    
    # Update session data
    session['timestamp'] = current_time
    session['last_request'] = current_time
    session['request_count'] += 1
    
    return True

def search_products(query: str) -> List[dict]:
    """Search products by name or category"""
    q = (query or "").lower()
    return [
        item for item in ITEMS
        if q in (item.get('name', '').lower()) or q in (item.get('category', '').lower())
    ]

def search_faq(query: str) -> List[dict]:
    """Search FAQ by question or answer"""
    q = (query or "").lower()
    return [
        faq for faq in FAQ_DATA
        if q in faq['q'].lower() or q in faq['a'].lower()
    ]

def analyze_sentiment(text: str) -> dict:
    """Simple sentiment analysis"""
    positive_words = {"great", "good", "excellent", "happy", "satisfied", "thanks", "love"}
    negative_words = {"bad", "poor", "terrible", "unhappy", "disappointed", "complaint", "issue"}
    
    words = set(text.lower().split())
    pos_count = len(words.intersection(positive_words))
    neg_count = len(words.intersection(negative_words))
    
    if pos_count > neg_count:
        return {"sentiment": "positive", "confidence": min(1.0, pos_count / len(words) + 0.5)}
    elif neg_count > pos_count:
        return {"sentiment": "negative", "confidence": min(1.0, neg_count / len(words) + 0.5)}
    return {"sentiment": "neutral", "confidence": 0.5}

def categorize_ticket(text: str) -> dict:
    """Categorize support ticket based on content"""
    categories = {
        "Order Issues": ["order", "purchase", "bought"],
        "Returns": ["return", "refund", "money back"],
        "Product Information": ["specs", "details", "information"],
        "Technical Support": ["error", "not working", "broken"],
        "Shipping": ["delivery", "shipping", "track"],
        "Account": ["login", "password", "account"],
    }
    
    text = text.lower()
    max_matches = 0
    best_category = "General Inquiry"
    
    for category, keywords in categories.items():
        matches = sum(1 for keyword in keywords if keyword in text)
        if matches > max_matches:
            max_matches = matches
            best_category = category
    
    return {
        "category": best_category,
        "confidence": min(1.0, max_matches * 0.2 + 0.5)
    }

# Blueprint setup
mcp = Blueprint("mcp", __name__, url_prefix="/mcp")

# Endpoints
@mcp.route("/session/open", methods=["POST"])
@handle_errors
def session_open():
    """Create or resume a session"""
    body = request.get_json(force=True) or {}
    session_id = body.get("session_id", str(uuid.uuid4()))
    
    # Initialize or update session
    active_sessions[session_id] = {
        "timestamp": time.time(),
        "request_count": 0,
        "last_request": time.time()
    }
    
    logger.info(f"Session opened: {session_id}")
    
    return jsonify({
        "ok": True,
        "session_id": session_id,
        "capabilities": {
            "context": [
                "products",
                "orders",
                "returns",
                "faq",
                "tickets",
                "categories"
            ],
            "tools": [
                "search_products",
                "check_order",
                "check_return_eligibility",
                "search_faq",
                "analyze_sentiment",
                "categorize_ticket"
            ]
        }
    }), 200

@mcp.route("/context/request", methods=["POST"])
@handle_errors
def context_request():
    """Handle context requests"""
    body = request.get_json(force=True) or {}
    session_id = body.get("session_id")
    request_id = body.get("request_id", str(uuid.uuid4()))
    resource = body.get("resource")
    
    if not session_id or not validate_session(session_id):
        return jsonify({
            "type": "context.response",
            "request_id": request_id,
            "error": "invalid_session"
        }), 401
    
    logger.info(f"Context request: {resource} (session: {session_id})")
    
    if resource == "products":
        return jsonify({
            "type": "context.response",
            "request_id": request_id,
            "data": ITEMS
        }), 200
    
    elif resource == "faq":
        return jsonify({
            "type": "context.response",
            "request_id": request_id,
            "data": FAQ_DATA
        }), 200
    
    elif resource == "categories":
        return jsonify({
            "type": "context.response",
            "request_id": request_id,
            "data": TICKET_CATEGORIES
        }), 200
    
    elif resource == "orders":
        # Mock order data
        orders = [
            {
                "id": "ORD12345",
                "status": "Shipped",
                "customer": "Jane Doe",
                "items": [{"id": "ELC12", "quantity": 1}],
                "date": "2025-09-20"
            }
        ]
        return jsonify({
            "type": "context.response",
            "request_id": request_id,
            "data": orders
        }), 200
    
    return jsonify({
        "type": "context.response",
        "request_id": request_id,
        "error": "resource_not_found"
    }), 404

@mcp.route("/tool/run", methods=["POST"])
@handle_errors
def tool_run():
    """Execute tools"""
    body = request.get_json(force=True) or {}
    session_id = body.get("session_id")
    request_id = body.get("request_id", str(uuid.uuid4()))
    tool = body.get("tool")
    inputs = body.get("input", {})
    
    if not session_id or not validate_session(session_id):
        return jsonify({
            "type": "tool.result",
            "request_id": request_id,
            "error": "invalid_session"
        }), 401
    
    logger.info(f"Tool request: {tool} (session: {session_id})")
    
    if tool == "search_products":
        results = search_products(inputs.get("q", ""))
        return jsonify({
            "type": "tool.result",
            "request_id": request_id,
            "output": results
        }), 200
    
    elif tool == "search_faq":
        results = search_faq(inputs.get("q", ""))
        return jsonify({
            "type": "tool.result",
            "request_id": request_id,
            "output": results
        }), 200
    
    elif tool == "analyze_sentiment":
        text = inputs.get("text", "")
        result = analyze_sentiment(text)
        return jsonify({
            "type": "tool.result",
            "request_id": request_id,
            "output": result
        }), 200
    
    elif tool == "categorize_ticket":
        text = inputs.get("text", "")
        result = categorize_ticket(text)
        return jsonify({
            "type": "tool.result",
            "request_id": request_id,
            "output": result
        }), 200
    
    return jsonify({
        "type": "tool.result",
        "request_id": request_id,
        "error": "unknown_tool"
    }), 400

@mcp.route("/session/close", methods=["POST"])
@handle_errors
def session_close():
    """Close a session"""
    body = request.get_json(force=True) or {}
    session_id = body.get("session_id")
    
    if session_id in active_sessions:
        del active_sessions[session_id]
        logger.info(f"Session closed: {session_id}")
        return jsonify({"ok": True}), 200
    
    return jsonify({
        "ok": False,
        "error": "session_not_found"
    }), 404