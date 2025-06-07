from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Asset
from . import db

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/')
@login_required
def list_assets():
    assets = Asset.query.all()
    return render_template('list_assets.html', assets=assets)

@asset_bp.route('/asset/create', methods=['GET', 'POST'])
@login_required
def create_asset():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        name = request.form['name']
        asset_type = request.form['asset_type']
        serial_number = request.form['serial_number']
        location = request.form['location']
        if not all([name, asset_type, serial_number, location]):
            flash('All fields required')
            return redirect(url_for('asset.create_asset'))
        if Asset.query.filter_by(serial_number=serial_number).first():
            flash('Serial number must be unique')
            return redirect(url_for('asset.create_asset'))
        asset = Asset(name=name, asset_type=asset_type,
                      serial_number=serial_number, location=location,
                      owner_id=current_user.id)
        db.session.add(asset)
        db.session.commit()
        flash('Asset created')
        return redirect(url_for('asset.list_assets'))
    return render_template('asset_form.html', action='Create')

@asset_bp.route('/asset/<int:asset_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    if request.method == 'POST':
        asset.name = request.form['name']
        asset.asset_type = request.form['asset_type']
        asset.serial_number = request.form['serial_number']
        asset.location = request.form['location']
        db.session.commit()
        flash('Asset updated')
        return redirect(url_for('asset.list_assets'))
    return render_template('asset_form.html', action='Edit', asset=asset)

@asset_bp.route('/asset/<int:asset_id>/delete', methods=['POST'])
@login_required
def delete_asset(asset_id):
    if current_user.role != 'admin':
        flash('Only admin can delete assets')
        return redirect(url_for('asset.list_assets'))
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash('Asset deleted')
    return redirect(url_for('asset.list_assets'))
