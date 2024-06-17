    # Verifica se a entrada é uma URL ou um título de música
    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        # Se for um título de música, pesquisa no YouTube
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
            # Pesquisa no YouTube pelo título fornecido
            search_query = f"ytsearch1:{query}"
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info:
                    url = info['entries'][0]['url']  # Pega o link da primeira entrada dos resultados
                else:
                    await ctx.send("Nenhum resultado encontrado para a pesquisa.")
                    return

        except youtube_dl.utils.DownloadError:
            await ctx.send("Ocorreu um erro ao tentar extrair a URL do vídeo. Certifique-se de que o título está correto.")
            return
