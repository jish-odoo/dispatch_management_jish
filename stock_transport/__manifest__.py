{
    "name" : "Transport Management System",
    "description": "Task for test",
    "version": '17.0.1.0.0',
    "author": "Jinay Shah(JISH)",
    "depends" : ["stock_picking_batch", "fleet", "web_gantt"],
    "installable": True,
    "license": "LGPL-3",
    "data": [
        'security/ir.model.access.csv',
        "views/fleet_vehicle_model_category_view.xml",
        "views/stock_picking_batch_view.xml",
        "views/stock_picking_view.xml"
    ]
}