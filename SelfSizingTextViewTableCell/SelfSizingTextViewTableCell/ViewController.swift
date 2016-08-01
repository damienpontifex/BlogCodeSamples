//
//  ViewController.swift
//  SelfSizingTextViewTableCell
//
//  Created by Damien Pontifex on 1/10/2014.
//  Copyright (c) 2014 Damien Pontifex. All rights reserved.
//

import UIKit

class ViewController: UITableViewController {

	override func viewDidLoad() {
		super.viewDidLoad()
		
		tableView.register(UINib(nibName: "MultiLineTextInputTableViewCell", bundle: nil), forCellReuseIdentifier: "MultiLineTextInputTableViewCell")
        tableView.keyboardDismissMode = .onDrag
	}
}

//MARK: - UITableViewDataSource
extension ViewController {
	override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return 1
	}
	
	override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(withIdentifier: "MultiLineTextInputTableViewCell", for: indexPath) as! MultiLineTextInputTableViewCell
		cell.titleLabel?.text = "Multi line cell"
		cell.textString = "Test String\nAnd another string\nAnd another"
		return cell
	}
	
	override func tableView(_ tableView: UITableView, estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat {
		return 44.0
	}
	
	override func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return UITableViewAutomaticDimension
	}
}
