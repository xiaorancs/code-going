# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request, jsonify
from flask import session
import random
import time
import os
import sys

# from percolation import PercolationStats, Percolation
# from puzzle import Board, Solver
# from autocomplete import Autocomplete
# from kdtree import Point2D, RectHV, KdTree
# from worknet import WorkNet, Outcast
import numpy as np

SECRET_KEY = 'algo_gogogo'
app = Flask(__name__)
app.secret_key = SECRET_KEY

# autocomplete_app = None
# kd_tree = None
# work_net = None
# outcast = None

@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route('/percolate')
def percolate():
    print("session ...... ......", session['name'], session['app_source_dir'])
    return render_template('/percolation/index.html')

@app.route('/percolate_do')
def percolate_do():
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    
    if session['app_source_dir'] not in sys.path:    
        sys.path.append(session['app_source_dir'])

    if not os.path.exists(os.path.join(session['app_source_dir'], "percolation.py")):
        print(os.path.join(session['app_source_dir'], "percolation.py"))
        return render_template('404.html')
    print("===========================================")
    try:
        from percolation import PercolationStats, Percolation

        n = int(request.args.get('n'))
        t = int(request.args.get('t'))

        test_result = []
        percolation_stats = PercolationStats(n, t)
        mean, std, low_conf, high_conf, percolation_status = percolation_stats.run()
        if type(percolation_status) is np.ndarray:
            percolation_status = percolation_status.tolist()
        
        print("xiaoran", mean, std, low_conf, high_conf,)
        test_result = [n, t, mean, std, low_conf, high_conf]
        data = {"result": {
            "answer": test_result,
            "data": percolation_status
        }}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "percolation.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)

@app.route('/puzzle')
def puzzle():
    return render_template('/puzzle/index.html')


@app.route('/puzzle_do')
def puzzle_do():
    print("------------------")
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')

    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    if not os.path.exists(os.path.join(session['app_source_dir'], "puzzle.py")):
        print(os.path.join(session['app_source_dir'], "puzzle.py"))
        return render_template('404.html')
    try:
        from puzzle import Board, Solver
        
        puzzle_id = request.args.get('puzzle_id')
        print("puzzle_id", puzzle_id)

        random_list = [0,1,2,4,5,3,7,8,6]
        n = 3
        if int(puzzle_id) == 3:
            n = 3
            random_lists = [
                [1,0,2,4,6,3,7,5,8],
                [1,2,3,0,4,8,7,6,5],
                [1,3,5,7,2,6,8,0,4],
                [4,1,2,3,0,6,5,7,8],
                [5,2,1,4,8,3,7,6,0],
                [8,3,5,6,4,2,1,0,7],
                # [8,6,7,2,0,4,3,5,1]
            ]
            random_list = random_lists[random.randint(0, len(random_lists)-1)]

        if int(puzzle_id) == 4:
            n = 4
            random_lists = [
                [1,6,2,4,5,0,3,8,9,10,7,11,13,14,15,12],
                [1,2,3,4,6,10,7,8,5,0,11,12,9,13,14,15],
                [5,1,3,4,9,2,7,8,13,0,10,12,14,6,11,15],
                [5,2,4,0,6,1,3,8,13,11,7,12,10,9,14,15],
                [6,3,7,4,2,9,10,8,1,5,12,15,13,0,14,11],
                [1,2,3,4,5,6,7,8,10,0,11,12,9,13,14,15],
                [9,5,1,2,6,4,8,3,10,14,7,11,13,0,15,12],
                [2,4,8,12,1,7,3,14,0,6,15,11,5,9,13,10]
            ]
            random_list = random_lists[random.randint(0, len(random_lists)-1)]

        if int(puzzle_id) == 5:
            n = 5
            random_lists = [
                [1,2,3,4,5,12,6,8,9,10,0,7,13,19,14,11,16,17,18,15,21,22,23,24,20],
                [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,16,17,18,19,21,22,23,24,20]
            ]
            random_list = random_lists[random.randint(0, len(random_lists)-1)]

        # random.shuffle(random_list)
        board_data = np.array(random_list).reshape(n, n)
        board = Board(board_data)

        solver = Solver(board)
        solver.solver()
        # print(solver.moves())
        # print(solver.solution())
        data_set = np.array(solver.solution())
        print("================== dataset =============", data_set)
        data_size = len(data_set)

        data = {"result": {
            "data_set": data_set.tolist(),
            "data_size": data_size
        }}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "puzzle.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get('query')
    data_set = ["我是", "我是谁", "我是你"]
    if query == 'a':
        data_set = ["Ni shi"]
    print(request.args)
    return render_template('/autocomplete/index.html', data=data_set)

@app.route("/autocomplete_do")
def autocomplete_do():
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "autocomplete.py")):
        print(os.path.join(session['app_source_dir'], "autocomplete.py"))
        return render_template('404.html')
    
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    try:
        from autocomplete import Autocomplete

        autocomplete_app = Autocomplete("./static/wiktionary.txt")
        autocomplete_app.create_dict_tree()

        top_k = 10
        query = request.args.get('query')
        print(query)
        data = {"result":[('a', 10), ('aa', '8')]}
        ans = autocomplete_app.tree.search_prefix(query)
        data = {"result": ans[:]}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "autocomplete.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


@app.route("/kdtree")
def kdtree():
    return render_template('/kdtree/index.html')


@app.route("/kdtree_search")
def kdtree_search():
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "kdtree.py")):
        print(os.path.join(session['app_source_dir'], "kdtree.py"))
        return render_template('404.html')
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    try:
        from kdtree import Point2D, RectHV, KdTree
        kd_tree = KdTree("./static/kdtree/input1M.txt", k=10000)
        kd_tree.construct_kdtree()
        top_k = 10
        x = request.args.get('x')
        y = request.args.get('y')
        print(x, y)

        data = {"result":[('a', 10), ('aa', '8')]}
        min_dist, target = kd_tree.nearest(Point2D(float(x), float(y)))
        data = {"result": {
            "min_dist": min_dist,
            "point": "(%s, %s)" % (target.x, target.y)
        }}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "kdtree.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


@app.route("/kdtree_range")
def kdtree_range():
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "kdtree.py")):
        print(os.path.join(session['app_source_dir'], "kdtree.py"))
        return render_template('404.html')
    if session['app_source_dir'] not in sys.path:    
        sys.path.append(session['app_source_dir'])
    try:
        from kdtree import Point2D, RectHV, KdTree
        kd_tree = KdTree("./static/kdtree/input1M.txt", k=10000)
        kd_tree.construct_kdtree()

        xmin = float(request.args.get('xmin'))
        ymin = float(request.args.get('ymin'))
        xmax = float(request.args.get('xmax'))
        ymax = float(request.args.get('ymax'))

        res = kd_tree.range(rect=RectHV(xmin, ymin, xmax, ymax))
        print(res[:10])
        now = int(time.time())
        file_name = "./static/kdtree/range_%s.jpg" % (now)
        kd_tree.plot_fig(res, xmin, ymin, xmax, ymax, file_name)
        data = {"result": {
            "img_src": "/static/kdtree/range_%s.jpg" % (now)
        }}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "kdtree.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)

@app.route("/worknet")
def worknet():
    return render_template('/worknet/index.html')

@app.route("/worknet_outcast")
def worknet_outcast():
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "worknet.py")):
        print(os.path.join(session['app_source_dir'], "worknet.py"))
        return render_template('404.html')
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    try:
        from worknet import WorkNet, Outcast

        work_net = WorkNet(synsets_file="./static/worknet/synsets.txt", hypernyms_file="./static/worknet/hypernyms.txt")
        work_net.init_worknet()
        outcast = Outcast(word_net=work_net)

        print("++++++++++++++=")
        input = request.args.get('input')
        input = input.split(",")
        best_noun, max_dist = outcast.outcast(nouns=input)

        data = {"result": {
            "max_dist": max_dist,
            "img_src": "/static/worknet/%s.webp" % (best_noun)
        }}
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "worknet.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    print("-----------------")
    if request.method == 'POST':
        print("++++++++", request, request.files)
        try:
            f = request.files['file']
            name = request.form.get('name')
            if name == "":
                return render_template('404.html')
            file_dir = "data/%s" % name 
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            file_name = f.filename
            print("file_name", file_name)
            if file_name in ["percolation.py", "puzzle.py", "calculator.py", "adv_calculator.py"] and name in ["xiaoran"]:
                return render_template('404.html')
            if not file_name.endswith(".py"):
                return render_template('404.html')
            file_name = os.path.join(file_dir, file_name)
            f.save(file_name)
            session['name'] = name
            session['app_source_dir'] = os.path.join("/home/xiaoran/works2021/cos226_web/flaskr", file_dir)
            print("name", name)
            print("session", session)
            data = {
                "result": "hahaha"
            }
            return render_template('base.html')
        except:
            return render_template('404.html')


@app.route('/calculator')
def calculator():
    return render_template('./calculator/index.html')

@app.route('/calculator_do')
def calculator_do():
    input = request.args.get('input')
    print(input)
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "calculator.py")):
        print(os.path.join(session['app_source_dir'], "calculator.py"))
        return render_template('404.html')
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    try:
        from calculator import Calculator

        calcul = Calculator()
        ans = calcul.solver(input)
        data = {
            'result': {
                'ans': ans
            }
        }
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "calculator.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


@app.route('/calculator_adv')
def calculator_adv():
    return render_template('./calculator/index_adv.html')

@app.route('/calculator_adv_do')
def calculator_adv_do():
    input = request.args.get('input')
    print(input)
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    # if not os.path.exists(os.path.join(session['app_source_dir'], "adv_calculator.py")):
    #     print("log 1", os.path.join(session['app_source_dir'], "adv_calculator.py"))
    #     return render_template('404.html')
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    print("sys.path", sys.path)
    try:
        try:
            from adv_calculator import AdvCalculator
        except:
            from adv_caculator import AdvCalculator
        calcul = AdvCalculator()
        ans = calcul.solver(input)
        print("==========ans===========", ans)
        data = {
            'result': {
                'ans': ans
            }
        }
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "adv_calculator.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)

@app.route("/autocheck")
def autocheck():
    return render_template('/autocheck/index.html')

@app.route("/autocheck_do")
def autocheck_do():
    query = request.args.get('query')
    print("session ...... ......", session['name'], session['app_source_dir'])
    if 'name' not in session or session['name'] is None:
        return render_template('404.html')
    if not os.path.exists(os.path.join(session['app_source_dir'], "autocheck.py")):
        print(os.path.join(session['app_source_dir'], "autocheck.py"))
        return render_template('404.html')
    if session['app_source_dir'] not in sys.path:
        sys.path.append(session['app_source_dir'])
    try:
        from autocheck import AutoCheck
        auto_check = AutoCheck(word_file="./static/autocheck/words.txt")
        hint_query = auto_check.auto_check(query)
        data = {
            'result': {
                'answer': hint_query
            }
        }
        return jsonify(response=data)
    except Exception as e:
        data = {"result": {
            "exception": "autocheck.py: " +  str(e)
        }}
        print("exception=========", e, data)
        return jsonify(response=data)


if __name__ == '__main__':
    # autocomplete = Autocomplete("./static/wiktionary.txt")
    # autocomplete.create_dict_tree()

    # 初始化kdtree
    # kd_tree = KdTree("./static/kdtree/input1M.txt", k=10000)
    # kd_tree.construct_kdtree()

    # 初始化worknet
    # work_net = WorkNet(synsets_file="./static/worknet/synsets.txt", hypernyms_file="./static/worknet/hypernyms.txt")
    # work_net.init_worknet()
    # outcast = Outcast(word_net=work_net)

    app.run("127.0.0.1", port=5000, debug=True)