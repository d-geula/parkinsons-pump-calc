def calculate_vial_duration(
    vial_amount: float, 
    base_flow_rate: float, 
    boost_flow_rate: float, 
    night_flow_rate: float, 
    expected_boosts: int, 
    night_hours: int
):
    """
    Calculate the estimated duration of a vial of medication.
    
    Args:
        vial_amount: The amount of medication available to the pump (ml).
        base_flow_rate: The pump flow rate during the day (ml/hr).
        boost_flow_rate: The pump flow rate during a boost (ml, instantaneous).
        night_flow_rate: The pump flow rate during the night (ml/hr).
        expected_boosts: The expected number of boosts.
        night_hours: The number of hours during the night.
    """
    # Calculate total boost consumption and subtract from vial amount
    boost_consumption = boost_flow_rate * expected_boosts
    remaining_amount = vial_amount - boost_consumption
    
    # Calculate night consumption
    night_consumption = night_flow_rate * night_hours
    
    # Calculate remaining amount after night hours
    remaining_amount -= night_consumption
    
    # Calculate how many hours the remaining amount will last
    base_rate_hours = remaining_amount / base_flow_rate
    
    # Calculate total hours
    total_hours = base_rate_hours + night_hours
    
    
    return {
        "estimated_hours": total_hours,
        "day_consumption": base_rate_hours * base_flow_rate,
        "night_consumption": night_consumption,
        "boost_consumption": boost_consumption,
    }
    