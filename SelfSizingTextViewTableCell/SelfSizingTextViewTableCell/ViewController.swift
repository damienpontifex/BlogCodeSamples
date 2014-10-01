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
		
		tableView.registerNib(UINib(nibName: "MultiLineTextInputTableViewCell", bundle: nil)!, forCellReuseIdentifier: "MultiLineTextInputTableViewCell")
		
		tableView.rowHeight = UITableViewAutomaticDimension
		tableView.estimatedRowHeight = 44.0
	}
}

extension ViewController: UITableViewDataSource {
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return 1
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("MultiLineTextInputTableViewCell", forIndexPath: indexPath) as MultiLineTextInputTableViewCell
		cell.titleLabel.text = "Multi line cell"
		cell.textString = "Test String\nAnd another string\nAnd another"
		return cell
	}
}