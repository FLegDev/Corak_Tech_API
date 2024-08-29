import re
from decimal import Decimal
from django.utils import timezone
from .models import Custom, Promotion, Product
import logging

logger = logging.getLogger(__name__)

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        logger.warning(f"{model.__name__} does not exist for parameters {kwargs}")
        return None

def get_promotion_symbol(instance):
    symbol = {'REM': '%', 'RED': '€', 'PME': ' EN avantage carte'}.get(instance.CSTTOT_KEY, '')
    logger.debug(f"Promotion symbol for {instance.CSTTOT_KEY}: {symbol}")
    return symbol

def calculate_discounted_price(instance, promotion_value, original_price, promotion_message):
    if instance.CSTTOT_KEY == 'REM':
        discounted_price = original_price * (1 - promotion_value / 100)
    elif instance.CSTTOT_KEY == 'RED':
        discounted_price = original_price - promotion_value
    elif "1+1" in promotion_message:
        discounted_price = original_price / 2
    else:
        discounted_price = original_price
    logger.debug(f"Calculated discounted price for {instance.code_article}: {discounted_price}")
    return discounted_price

def get_promotion_times_as_string(promotion):
    pro_start_time_str = promotion.start.strftime("%Y-%m-%d %H:%M:%S") if promotion.start else ""
    pro_end_time_str = promotion.end.strftime("%Y-%m-%d %H:%M:%S") if promotion.end else ""
    logger.debug(f"Promotion times for {promotion.code_article}: start={pro_start_time_str}, end={pro_end_time_str}")
    return pro_start_time_str, pro_end_time_str

def determine_message(instance):
    advantage, condition, message_fid, info_panachage = "", "", "", ""
    if instance.ADVCARACT_AMOUNT < 10000 and instance.CSTTOT_KEY == "REM":
        advantage = f"Remise {instance.ADVCARACT_AMOUNT / 100}%"
    elif instance.ADVCARACT_AMOUNT == 10000:
        if instance.ADVCARACT_MIN == 100:
            advantage = "1 offert"
        else:
            advantage = f"{instance.ADVCARACT_MIN // 100}+1 offerts"
    elif instance.CSTTOT_KEY == "RED":
        advantage = f"- {instance.ADVCARACT_AMOUNT / 100} €"
    elif instance.CSTTOT_KEY == "PME" and instance.BINID == "1" and instance.ADVTYPE_ID == "4":
        advantage = f"{instance.ADVCARACT_AMOUNT / 100} €"
    elif instance.CSTTOT_KEY == "PME" and instance.BINID == "1" and instance.ADVTYPE_ID == "3":
        advantage = f"{instance.ADVCARACT_AMOUNT / 100} %"
    if instance.ADVCARACT_AMOUNT < 10000 and instance.ADVCARACT_MIN == 100 and instance.CSTTOT_KEY != "PME":
        condition = "En caisse"
    elif instance.ADVCARACT_AMOUNT < 10000 and instance.ADVCARACT_MIN > 100:
        condition = "SUR LE 2 ème" if instance.ADVCARACT_MIN == 200 else "SUR LE 3 ème" if instance.ADVCARACT_MIN == 300 else "SUR LE 4 ème"
    elif instance.ADVCARACT_AMOUNT < 1000 and instance.CSTTOT_KEY != "PME":
        condition = "En caisse"
    elif instance.ADVCARACT_AMOUNT == 10000:
        condition = "Offert"
    if instance.BINID == "1" and instance.CSTTOT_KEY == "REM":
        message_fid = "Avec la carte de fidélité"
    elif instance.BINID == "1" and instance.CSTTOT_KEY == "PME":
        message_fid = "Crédité sur la carte de fidélité"
    if instance.ADVCARACT_MIN > 100 and (instance.ADV_PROFIL == 'P011' or instance.ADV_PROFIL == 'P419'):
        info_panachage = f"*Panachage possible. Remise sur le moins cher des {instance.ADVCARACT_MIN // 100}."
    message = ' '.join(filter(None, [advantage, condition, message_fid, info_panachage]))
    logger.debug(f"Determined messages for {instance.code_article}: {message}, {condition}, {message_fid}, {info_panachage}")
    return message, condition, message_fid, info_panachage

def split_promotion_message(promotion_message):
    discount_percentage, discount_amount, details = "", "", ""
    percentage_match = re.search(r"(\d+\.\d+%)", promotion_message)
    if percentage_match:
        discount_percentage = percentage_match.group(1).replace(".0%", "%")
    amount_match = re.search(r"(\d+€)", promotion_message)
    if amount_match:
        discount_amount = amount_match.group(1)
    details_match = re.search(r"\*(.*)", promotion_message)
    if details_match:
        details = details_match.group(1).replace(".0", "")
    logger.debug(f"Split promotion message: {discount_percentage}, {discount_amount}, {details}")
    return discount_percentage or discount_amount, discount_amount, details

def handle_custom_save(instance, created):
    code_article = instance.code_article
    promotion_message, condition, message_fid, info_panachage = determine_message(instance)

    try:
        product = Product.objects.get(code_article=code_article)
        product.promo_message = promotion_message
        product.promo_condition = condition
        product.promo_fid_card_message = message_fid
        product.promo_mixing_message = info_panachage
        product.save()
        logger.info(f"Updated Product instance {product.id} with promo message: {promotion_message}")
    except Product.DoesNotExist:
        logger.warning(f"Product with code_article {code_article} does not exist.")
        return
    except Exception as e:
        logger.error(f"Error updating Product for code_article {code_article}: {e}")
