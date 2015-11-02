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
		
		tableView.registerNib(UINib(nibName: "MultiLineTextInputTableViewCell", bundle: nil), forCellReuseIdentifier: "MultiLineTextInputTableViewCell")
	}
}

//MARK: - UITableViewDataSource
extension ViewController {
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return 1
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("MultiLineTextInputTableViewCell", forIndexPath: indexPath) as! MultiLineTextInputTableViewCell
		cell.titleLabel?.text = "Multi line cell"
		cell.textString = "Test String\nAnd another string\nAnd another"
		return cell
	}
	
	override func tableView(tableView: UITableView, estimatedHeightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
		return 44.0
	}
	
	override func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
		return UITableViewAutomaticDimension
	}
}