//
//  MultiLineTextInputTableViewCell.swift
//  ER Pro
//
//  Created by Damien Pontifex on 7/08/2014.
//  Copyright (c) 2014 Evoque Rehab. All rights reserved.
//

import UIKit

class MultiLineTextInputTableViewCell: UITableViewCell {
	
	@IBOutlet weak var titleLabel: UILabel?
    @IBOutlet var textView: UITextView?
	
    override init(style: UITableViewCellStyle, reuseIdentifier: String!) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
    }
    
    required init(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
	
	/// Custom setter so we can initialise the height of the text view
	var textString: String {
		get {
			return textView?.text ?? ""
		}
		set {
			textView?.text = newValue
			
			textViewDidChange(textView)
		}
	}

    override func awakeFromNib() {
        super.awakeFromNib()
		
		// Disable scrolling inside the text view so we enlarge to fitted size
        textView?.scrollEnabled = false
        textView?.delegate = self
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        if selected {
            textView?.becomeFirstResponder()
        } else {
            textView?.resignFirstResponder()
        }
    }
}

extension MultiLineTextInputTableViewCell: UITextViewDelegate {
    func textViewDidChange(textView: UITextView!) {
		
		// Only way found to make table view update layout of cell
		// More efficient way?
		
		tableView?.beginUpdates()
		tableView?.endUpdates()
    }
}
