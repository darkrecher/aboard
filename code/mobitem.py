
from position import Pos


class MobileItem():

	# TODO : les params, c'est totalement nawak. Faut arranger ça autrement.

	def __init__(
		self,
		board_owner=None, tile_owner=None, z_index=None,
		*args, **kwargs
	):
		self.tile_owner = None
		self.data = '#'
		self.move(board_owner, tile_owner, z_index, *args, **kwargs)


	def move(
		self,
		board_owner=None, tile_owner=None, z_index=None,
		*args, **kwargs
	):
		"""
		Param prioritaire : tile_owner.
		Sinon : les autres params.
		"""
		# FUTURE : j'ai plein de fonctions qui crée une pos à partir de args et kwargs.
		# Y'aurait peut-être moyen de le factoriser avec un décorateur.

		if self.tile_owner is not None:
			# --- suppression du mobitem de la tile où il était avant ---
			# Si self n'est pas mobile_items, ça va raiser une exception.
			# C'est ce qu'on veut, parce que not supposed to happen.
			index_myself = self.tile_owner.mobile_items.index(self)
			del self.tile_owner.mobile_items[index_myself]
			# --- définition éventuelle de board_owner, à partir de l'actuel board_owner ---
			if board_owner is None:
				board_owner = self.tile_owner.board_father

		# --- définition éventuelle de board_owner, à partir du nouveau tile_owner ---
		if tile_owner is not None:
			board_owner = tile_owner.board_father

		# --- définition éventuelle de tile_owner, à partir de board_owner et des param de pos ---
		if tile_owner is None and board_owner is not None:
			try:
				pos = Pos(*args, **kwargs)
				tile_owner = board_owner[pos]
			except:
				tile_owner = None

		# --- Enregistrement dans le nouveau tile_owner, si défini ---
		if tile_owner is not None:
			self.tile_owner = tile_owner
			if z_index is None:
				tile_owner.mobile_items.append(self)
			else:
				tile_owner.mobile_items.insert(z_index, self)


	def unlink(self):
		pass
		# TODO : c'est comme un move, mais avec tout à None.


	def render(self, w=1, h=1, chr_transparency=" "):
		return str(self.data)[:w]

