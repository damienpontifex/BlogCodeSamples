//
//  UITableViewCellExtensions.swift
//  SelfSizingTextViewTableCell
//
//  Created by Damien Pontifex on 1/10/2014.
//  Copyright (c) 2014 Damien Pontifex. All rights reserved.
//

import UIKit

extension UITableViewCell {
	/// Search up the view hierarchy of the table view cell to find the containing table view
	var tableView: UITableView? {
		get {
			var table: UIView? = superview
			while !(table is UITableView) && table != nil {
				table = table?.superview
			}
			
			return table as? UITableView
		}
	}
}