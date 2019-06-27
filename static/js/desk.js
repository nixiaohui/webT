$(function() {
    $("button#cmd").bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_start_game', {
        cmd: $('button#cmd').val()
      }, function(data) {
        if (data.cmd === 1) {
          $("button#cmd").text(data.result);
          $("button#cmd").attr("value",data.cmd);
          $("div.card-5").html(
              "<div class='card'>" +
              " <div class='" + data.player_cards[0]['value_ico'] + "'></div>" +
              " <div class='" + data.player_cards[0]['suit_ico'] + "'></div>" +
              " <div class='" + data.player_cards[0]['suit_image'] + "'></div>" +
              "</div>"+
              "<div class='card'>" +
              " <div class='" + data.player_cards[1]['value_ico'] + "'></div>" +
              " <div class='" + data.player_cards[1]['suit_ico'] + "'></div>" +
              " <div class='" + data.player_cards[1]['suit_image'] + "'></div>" +
              "</div>"
          );
          $("div.card-public").html("");
          $("div.card-turn").html("");
          $("div.card-river").html("");
        }
        else if (data.cmd === 2){
          $("button#cmd").attr("value",data.cmd);
          $("div.card-public").html(
              "<div class='card'>" +
              " <div class='" + data.flop_cards[0]['value_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[0]['suit_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[0]['suit_image'] + "'></div>" +
              "</div>"+
              "<div class='card'>" +
              " <div class='" + data.flop_cards[1]['value_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[1]['suit_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[1]['suit_image'] + "'></div>" +
              "</div>"+
              "<div class='card'>" +
              " <div class='" + data.flop_cards[2]['value_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[2]['suit_ico'] + "'></div>" +
              " <div class='" + data.flop_cards[2]['suit_image'] + "'></div>" +
              "</div>"
          );
          $("div.card-turn").html("");
          $("div.card-river").html("");
        }
        else if (data.cmd === 3){
          $("button#cmd").attr("value",data.cmd);
          $("div.card-turn").append(
              "<div class='card'>" +
              " <div class='" + data.turn_cards[0]['value_ico'] + "'></div>" +
              " <div class='" + data.turn_cards[0]['suit_ico'] + "'></div>" +
              " <div class='" + data.turn_cards[0]['suit_image'] + "'></div>" +
              "</div>"
          );
          $("div.card-river").html("");
        }
        else if (data.cmd === 4){
          $("button#cmd").text(data.result);
          $("button#cmd").attr("value", data.cmd);
          $("div.card-river").append(
              "<div class='card'>" +
              " <div class='" + data.river_cards[0]['value_ico'] + "'></div>" +
              " <div class='" + data.river_cards[0]['suit_ico'] + "'></div>" +
              " <div class='" + data.river_cards[0]['suit_image'] + "'></div>" +
              "</div>"
          );
        }
      });
      return false;
    });
});
