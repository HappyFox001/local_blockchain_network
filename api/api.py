from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os
import sys
import time
import subprocess

# Set up project root and import modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from node.node import Node
from core.methods.methods import hash
from network_manager import NetworkManager  # Adjust import path as needed

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Define database path and NetworkManager
DATABASE_PATH = "../db/blockchain.db"
manager = NetworkManager()

# Initialize nodes list
nodes = []


def get_latest_blocks(limit=50):
    """Retrieve the latest 'limit' blocks from the database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.execute(
            "SELECT height, block_hash, previous_hash, type FROM blocks ORDER BY height DESC LIMIT ?",
            (limit,),
        )
        blocks = [
            {
                "height": row[0],
                "block_hash": row[1],
                "previous_hash": row[2],
                "type": row[3],
            }
            for row in cursor.fetchall()
        ]
    return blocks[::-1]  # Return blocks in ascending order for frontend display


@app.route("/blocks", methods=["GET"])
def get_blocks():
    """API route to get the latest blocks, returns up to 50 blocks."""
    try:
        blocks = get_latest_blocks()
        return jsonify({"success": True, "blocks": blocks})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/start_mining", methods=["POST"])
def start_mining():
    """Start mining on all nodes."""
    try:
        manager.start_all_nodes_mining()
        return jsonify({"success": True, "message": "Mining started on all nodes."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/stop_mining", methods=["POST"])
def stop_mining():
    """Stop mining on all nodes."""
    try:
        manager.stop_all_nodes_mining()
        return jsonify({"success": True, "message": "Mining stopped on all nodes."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/restart_nodes", methods=["POST"])
def restart_nodes():
    """Restart all nodes."""
    try:
        # 执行 .sh 文件
        result = subprocess.run(
            ["restart.sh"], check=True, capture_output=True, text=True
        )
        print("ok")

        # 返回成功信息和脚本输出
        return jsonify(
            {
                "success": True,
                "message": "All nodes restarted.",
                "output": result.stdout,
            }
        )
    except subprocess.CalledProcessError as e:
        # 捕获脚本运行中的错误
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Error running restart script",
                    "error": e.stderr,
                }
            ),
            500,
        )
    except Exception as e:
        # 捕获其他异常
        return jsonify({"success": False, "message": str(e)}), 500


def start_nodes(num_nodes=5):
    """Initialize and start a given number of nodes."""
    for i in range(num_nodes):
        node = Node(name=f"Node{i}", manager=manager)
        manager.add_node(node)
        node.start()
        manager.start_node_mining(node.name)
        nodes.append(node)
    return nodes


if __name__ == "__main__":
    # Start the nodes
    nodes = start_nodes()

    # Start the Flask app
    app.run(debug=True)

    # Keep main thread running
    try:
        while True:
            time.sleep(1)
            # manager.store_block_info()  # Uncomment to store block information periodically
    except KeyboardInterrupt:
        print("Terminating nodes...")
