//+------------------------------------------------------------------+
//| QB_ExportCalendar: writes every high-impact economic calendar    |
//| event since InpFrom to Common\Files\QB\calendar_high.csv, so the |
//| research engine can backtest prop-firm news blackouts the way    |
//| QB_Host applies them live (the calendar is unavailable in the    |
//| Strategy Tester). Times are trade-server time, like bar times.   |
//| Run on a connected terminal; bridge/calendar.py automates it.    |
//+------------------------------------------------------------------+
#property strict
#property version "1.00"

input string InpFrom = "2019.01.01";
input int    InpWaitSec = 90;          // wait this long for the connection and calendar data

void OnStart()
{
   datetime from = StringToTime(InpFrom), to = TimeTradeServer() + 30 * 86400;
   MqlCalendarCountry countries[];
   int nc = 0;
   for(int i = 0; i < InpWaitSec * 2 && nc <= 0; i++)
   {
      if(TerminalInfoInteger(TERMINAL_CONNECTED)) nc = CalendarCountries(countries);
      if(nc <= 0) Sleep(500);
   }
   int h = FileOpen("QB\\calendar_high.tmp", FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(h == INVALID_HANDLE) { Print("QB_ExportCalendar: cannot open output file"); return; }
   FileWriteString(h, "time,currency,event\n");
   int rows = 0;
   for(int c = 0; c < nc; c++)
   {
      MqlCalendarEvent events[];
      int ne = CalendarEventByCountry(countries[c].code, events);
      for(int e = 0; e < ne; e++)
      {
         if(events[e].importance != CALENDAR_IMPORTANCE_HIGH) continue;
         MqlCalendarValue vals[];
         int nv = CalendarValueHistoryByEvent(events[e].id, vals, from, to);
         string name = events[e].name;
         StringReplace(name, ",", " ");
         for(int v = 0; v < nv; v++)
         {
            FileWriteString(h, StringFormat("%I64d,%s,%s\n", (long)vals[v].time, countries[c].currency, name));
            rows++;
         }
      }
   }
   FileClose(h);
   // Publish atomically so a failed run never leaves a truncated calendar behind.
   if(rows > 0 && FileMove("QB\\calendar_high.tmp", FILE_COMMON, "QB\\calendar_high.csv", FILE_COMMON | FILE_REWRITE))
      PrintFormat("QB_ExportCalendar: %d high-impact events from %d countries", rows, nc);
   else
      PrintFormat("QB_ExportCalendar: export failed (%d countries, %d rows)", nc, rows);
}
