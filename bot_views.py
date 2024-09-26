import datetime
import json
import threading
import time
from django.template.response import TemplateResponse
from .models import Setting, Trade
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging
import ccxt

from .serializers import TradeSerializer, SettingsSerializer

# Create a logger
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.INFO)
# Create a file handler
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.INFO)
# Create a formatter and set the format
formatter = logging.Formatter(f"datetime.now(pytz.timezone('Asia/Karachi')) - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(file_handler)

Passphrase = "/ZbfntBQyw2qV2$"


sett = Setting.objects.all().first()
settingSerializer = SettingsSerializer(sett)
setting = settingSerializer.data

okx = ccxt.okx({
    "apiKey":  setting['API_KEY'],
    "secret": setting['SECRET_KEY'],
    "password": setting['PASSPHRASE'],
    "options": {
        "defaultType": "spot",  # Or "linear" based on your account type
    }
})

CP = 0
signalB = 'None'
bot_running = False
bot_event = threading.Event()
current_side = 'None'
Pair = ''


def home(request):
    if not 0:
        return TemplateResponse(request, '404.html', {'error': 'Resource not found'}, status=404)
        # Return the resource if it exists
    return Response({'resource': 'found'})

def startBot():
    global CP, signalB, bot_running, bot_event, current_side, Pair
    # CP = okx.fetch_ticker(setting['pair'])["last"]
    while bot_running:
        bot_event.wait()  # Wait for the signal to start trading

        # CP = okx.fetch_ticker(setting['pair'])["last"]
        # print(CP)
        if signalB.lower() == 'buy' and current_side != 'buy':
            # Close existing sell order if present
            # if current_side == 'sell':
            #     print('Closing existing sell order')
            #     # open_positions = okx.fetch_position(setting['pair'])
            #     # side, size = open_positions['side'], open_positions['info']['size']
            #     data = okx.create_order(symbol=Pair, type=setting['orderType'], side='buy', amount=setting['trading_amount'],price=CP)
            #     Trade.objects.create(pair=Pair, orderType= setting['orderType'], side='buy', trading_amount= setting['trading_amount'], Data='Closing Sell Order')
            #     logger.info(f"CLOSE SELL {datetime.datetime.now()}")
            #     logger.info(f"data: {data}")
            #     current_side = 'None'
            sat = Setting.objects.all().first()
            satingSerializer = SettingsSerializer(sat)
            sating = satingSerializer.data
            CP = okx.fetch_ticker(setting['pair'])["last"]
            print(CP)
            # Open new buy order
            print('Opening new buy order')
            current_side = 'buy'
            signalB = 'None'
            # data = okx.create_order(Pair, sating['orderType'], 'buy', sating['trading_amount'], CP)
            Trade.objects.create(pair=Pair, orderType=sating['orderType'], side='buy', trading_amount=sating['trading_amount'], Data='Opening Buy Order')
            logger.info(f'settings {sating} \n')
            logger.info(f"{datetime.datetime.now()} BUY ORDER PLACED!!! \n")
            # logger.info(f"data: {data} \n")
            # SendTelegramBuyMessage(pair, CP, ema2)  # Uncomment and define this function if needed
            # print('Telegram buy message sent')


        elif signalB.lower() == 'sell' and current_side != 'sell':
            sat = Setting.objects.all().first()
            satingSerializer = SettingsSerializer(sat)
            sating = satingSerializer.data
            # Close existing buy order if present
            # if current_side == 'buy':
            #     print('Closing existing buy order')
            #     # open_positions = okx.fetch_position(setting['pair'])
            #     # side, size = open_positions['side'], open_positions['info']['size']
            #     data = okx.create_order(symbol=Pair, type=setting['orderType'], side='sell', amount=setting['trading_amount'], price=CP)
            #     Trade.objects.create(pair=Pair, orderType= setting['orderType'], side='sell', trading_amount= setting['trading_amount'], Data='Closing Buy Order')
            #     logger.info(f"CLOSE BUY {datetime.datetime.now()}")
            #     logger.info(f"data: {data}")
            #     current_side = 'None'

            CP = okx.fetch_ticker(setting['pair'])["last"]
            # Open new sell order
            print('Opening new sell order')
            current_side = 'sell'
            signalB = 'None'
            # data = okx.create_order(Pair, sating['orderType'], 'sell', sating['trading_amount'], CP)
            Trade.objects.create(pair=Pair, orderType=sating['orderType'], side='sell', trading_amount=sating['trading_amount'], Data= 'Opening Sell Order')
            logger.info(f'setttings {sating} \n')
            logger.info(f"{datetime.datetime.now()} SELL ORDER PLACED!! \n")
            # logger.info(f"data: {data} \n")
            # SendTelegramSellMessage(pair, CP, ema2)  # Uncomment and define this function if needed
            # print('Telegram sell message sent')


        time.sleep(1)




# @api_view(['POST'])
# def indicatorA(request):
#     global pair, CP, signalA, ema1, ema2
#     if request.method == 'POST':
#         try:
#             raw_data = request.body.decode('utf-8').strip('"')
#             data = json.loads(raw_data)
#             print(data)
#             if 'Pair' in data:
#                 Pair = data['Pair']
#             if 'CP' in data:
#                 CP = data['CP']
#             if 'EMA1' in data:
#                 ema1 = data['EMA1']
#             if 'EMA2' in data:
#                 ema2 = data['EMA2']
#             if 'A' in data:
#                 signalA = data['A'].strip().lower()
#
#             logger.info(f'Signal received {time.time()},  Pair: {Pair}, CP: {CP}, A: {signalA}\n')
#             print(f'Signal received {time.time()},  Pair: {Pair}, CP: {CP}, A: {signalA}\n')
#             return Response(
#                 {'message': f'Signal received {time.time()},  Pair: {Pair}, CP: {CP}, A: {signalA}\n'}
#             )
#
#         except Exception as e:
#             return Response({"error": str(e)})

@api_view(['POST'])
def indicatorB(request):
    global Pair, CP, signalB, bot_running, bot_event
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8').strip('"')
            data = json.loads(raw_data)
            if 'Pair' in data:
                Pair = data['Pair']
            if 'B' in data:
                signalB = data['B']
            if not bot_running:
                bot_thread = threading.Thread(target=startBot)
                bot_running = True
                bot_event.set()
                bot_thread.start()
                print('bot started running', bot_running)
                logger.info('Bot started running.')
            print(f' Pair: {Pair}, B: {signalB}')
            logger.info(f' Pair: {Pair}, B: {signalB}')
            return Response({'message': f'Signal Received {time.time()}. Pair: {Pair}, B: {signalB}'})

        except Exception as e:
            return Response({"error": str(e)})



# def close_position(sides):
#     global current_side
#     global count
#     global bot_running
#
#     global EMA
#
#     global RSI, PrevRSI, RSI_color, RSI_prev_color
#
#     global RSI2, PrevRSI2, RSI2_color, RSI2_prev_color
#
#     global OB, start_price, end_price
#     global BB
#
#     okx.cancel_all_orders(symbol=setting.pair)
#     open_positions = okx.fetch_position(setting.pair)
#     side, size = open_positions['side'], open_positions['info']['size']
#     if sides.lower() == 'sell':
#         okx.create_order(setting.pair, type='market', amount=size, side='buy', params={'reduce_only': True})
#
#
#     elif sides.lower() == 'buy':
#         okx.create_order(setting.pair, type='market', amount=size, side='sell', params={'reduce_only': True})
#         current_side = 'None'
#         count = 0
#         RSI = 0
#         PrevRSI = 0
#         RSI_color = ''
#         RSI_prev_color = ''
#
#         RSI2 = 0
#         PrevRSI2 = 0
#         RSI2_color = ''
#         RSI2_prev_color = ''
#         BB = ''
#         OB = ''
#         start_price = 0
#         end_price = 0
#         threading.Event()
#         bot_running = False
#         print(
#             f'bot closed running - count: {count} - Current Side: {current_side} - EMA: {EMA} - BB: {BB} - OB: {OB} RSI: {RSI} - PrevRSI: {PrevRSI} - RSI_color: {RSI_color} - RSI_prev_color: {RSI_prev_color}\n')
#         print(f'RSI: {RSI} - PrevRSI: {PrevRSI} - RSI_color: {RSI_color} - RSI_prev_color: {RSI_prev_color}')
#         print(f'RSI2: {RSI2} - PrevRSI2: {PrevRSI2} - RSI2_color: {RSI2_color} - RSI2_prev_color: {RSI2_prev_color}')
#



# def startBot():
#     global Pair, CP, signalB, ema1, ema2, bot_running, bot_event, current_side
#
#     while bot_running:
#         bot_event.wait()  # Wait for the signal to start trading
#         CP = okx.fetch_ticker(setting['pair'])["last"]
#         print(CP)
#         if signalB.lower() == 'buy' and current_side != 'buy':
#             # Close existing sell order if present
#             if current_side == 'sell':
#                 print('Closing existing sell order')
#                 open_positions = okx.fetch_position(setting.pair)
#                 side, size = open_positions['side'], open_positions['info']['size']
#                 data = okx.create_order(setting['pair'], type=setting['orderType'], side='buy', amount=size, params={'reduce_only': True})
#                 Trade.objects.create(Pair=setting['pair'], orderType= setting['orderType'], side= side, trading_amount= setting['trading_amount'])
#                 logger.info(f"CLOSE SELL {datetime.datetime.now()}")
#                 logger.info(f"data: {data}")
#                 current_side = None
#
#             # Open new buy order
#             print('Opening new buy order')
#             data = okx.create_order(setting['pair'], setting['orderType'], 'buy', setting['trading_amount'], CP)
#             Trade.objects.create(pair=setting['pair'], orderType=setting['orderType'], side=signalB, trading_amount=setting['trading_amount'])
#             logger.info(f"BUY {datetime.datetime.now()}")
#             logger.info(f"data: {data}")
#             # SendTelegramBuyMessage(pair, CP, ema2)  # Uncomment and define this function if needed
#             # print('Telegram buy message sent')
#             current_side = 'buy'
#             signalB = None
#
#         elif signalB.lower() == 'sell' and current_side != 'sell':
#             # Close existing buy order if present
#             if current_side == 'buy':
#                 print('Closing existing buy order')
#                 open_positions = okx.fetch_position(setting.pair)
#                 side, size = open_positions['side'], open_positions['info']['size']
#                 Trade.objects.create(pair=setting['pair'], orderType= setting['orderType'], side= side, trading_amount= setting['trading_amount'])
#                 data = okx.create_order(setting['pair'], type=setting['orderType'], side='sell', amount=size, params={'reduce_only': True})
#                 logger.info(f"CLOSE BUY {datetime.datetime.now()}")
#                 logger.info(f"data: {data}")
#                 current_side = None
#
#             # Open new sell order
#             print('Opening new sell order')
#             data = okx.create_order(setting['pair'], setting['orderType'], 'sell', setting['trading_amount'], CP)
#             Trade.objects.create(pair=setting['pair'], orderType=setting['orderType'], side=signalB, trading_amount=setting['trading_amount'])
#             logger.info(f"SELL {datetime.datetime.now()}")
#             logger.info(f"data: {data}")
#             # SendTelegramSellMessage(pair, CP, ema2)  # Uncomment and define this function if needed
#             print('Telegram sell message sent')
#             current_side = 'sell'
#             signalB = None
#
#         bot_event.clear()  # Clear the event to wait for the next signal
#         print(f'Trade executed: {current_side} at {CP}')
#         logger.info(f'Trade executed: {current_side} at {CP}')




######################################## opening one order and closing previous order
# def startBot():
#     global CP, signalB, bot_running, bot_event, current_side, Pair
#
#     while bot_running:
#         bot_event.wait()  # Wait for the signal to start trading
#         CP = okx.fetch_ticker(setting['pair'])["last"]
#         print(CP)
#         if signalB.lower() == 'buy' and current_side != 'buy':
#             # Close existing sell order if present
#             if current_side == 'sell':
#                 print('Closing existing sell order')
#                 # open_positions = okx.fetch_position(setting['pair'])
#                 # side, size = open_positions['side'], open_positions['info']['size']
#                 data = okx.create_order(symbol=Pair, type=setting['orderType'], side='buy', amount=setting['trading_amount'],price=CP)
#                 Trade.objects.create(pair=Pair, orderType= setting['orderType'], side='buy', trading_amount= setting['trading_amount'], Data='Closing Sell Order')
#                 logger.info(f"CLOSE SELL {datetime.datetime.now()}")
#                 logger.info(f"data: {data}")
#                 current_side = 'None'
#
#             # Open new buy order
#             print('Opening new buy order')
#             data = okx.create_order(Pair, setting['orderType'], 'buy', setting['trading_amount'], CP)
#             Trade.objects.create(pair=Pair, orderType=setting['orderType'], side='buy', trading_amount=setting['trading_amount'], Data='Opening Buy Order')
#             logger.info(f'setttings {setting} \n')
#             logger.info(f"{datetime.datetime.now()} BUY ORDER PLACED!!! \n")
#             logger.info(f"data: {data} \n")
#             # SendTelegramBuyMessage(pair, CP, ema2)  # Uncomment and define this function if needed
#             # print('Telegram buy message sent')
#             current_side = 'buy'
#             signalB = 'None'
#
#         elif signalB.lower() == 'sell' and current_side != 'sell':
#
#             # Close existing buy order if present
#             if current_side == 'buy':
#                 print('Closing existing buy order')
#                 # open_positions = okx.fetch_position(setting['pair'])
#                 # side, size = open_positions['side'], open_positions['info']['size']
#                 data = okx.create_order(symbol=Pair, type=setting['orderType'], side='sell', amount=setting['trading_amount'], price=CP)
#                 Trade.objects.create(pair=Pair, orderType= setting['orderType'], side='sell', trading_amount= setting['trading_amount'], Data='Closing Buy Order')
#                 logger.info(f"CLOSE BUY {datetime.datetime.now()}")
#                 logger.info(f"data: {data}")
#                 current_side = 'None'
#
#
#             # Open new sell order
#             print('Opening new sell order')
#             data = okx.create_order(Pair, setting['orderType'], 'sell', setting['trading_amount'], CP)
#             Trade.objects.create(pair=Pair, orderType=setting['orderType'], side='sell', trading_amount=setting['trading_amount'], Data= 'Opening Sell Order')
#             logger.info(f'setttings {setting} \n')
#             logger.info(f"{datetime.datetime.now()} SELL ORDER PLACED!! \n")
#             logger.info(f"data: {data} \n")
#             # SendTelegramSellMessage(pair, CP, ema2)  # Uncomment and define this function if needed
#             # print('Telegram sell message sent')
#             current_side = 'sell'
#             signalB = 'None'
#
#         time.sleep(1)
#
