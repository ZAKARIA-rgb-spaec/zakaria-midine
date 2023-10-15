class NoAmmunitionError(Exception):
    pass

class OutOfRangeError(Exception):
    pass

class Arme:
    def __init__(self, rayon_action, munitions):
        self.rayon_action = rayon_action
        self.munitions = munitions

    def fire_at(self, x, y, z):
        if self.munitions <= 0:
            raise NoAmmunitionError("No ammunition left")

        if not self.is_target_in_range(x, y, z):
            raise OutOfRangeError("Target is out of range")

        self.munitions -= 1
        return "Target destroyed"

    def is_target_in_range(self, x, y, z):
        raise NotImplementedError("Subclasses must implement this method")

class LanceMissilesAntisurface(Arme):
    def __init__(self):
        super().__init__(rayon_action=100, munitions=50)

    def is_target_in_range(self, x, y, z):
        return z == 0

class LanceMissilesAntiair(Arme):
    def __init__(self):
        super().__init__(rayon_action=20, munitions=40)

    def is_target_in_range(self, x, y, z):
        return z > 0

class LanceTorpilles(Arme):
    def __init__(self):
        super().__init__(rayon_action=40, munitions=24)

    def is_target_in_range(self, x, y, z):
        return z <= 0

# Tests unitaires
def test_arma_lance_missiles_antisurface():
    arme = LanceMissilesAntisurface()
    assert arme.fire_at(50, 50, 0) == "Target destroyed"
    assert arme.munitions == 49

def test_arma_lance_missiles_antiair():
    arme = LanceMissilesAntiair()
    assert arme.fire_at(10, 10, 10) == "Target destroyed"
    assert arme.munitions == 39

def test_arma_lance_torpilles():
    arme = LanceTorpilles()
    assert arme.fire_at(0, 0, -10) == "Target destroyed"
    assert arme.munitions == 23

def test_arma_lance_missiles_antisurface_hors_de_portee():
    arme = LanceMissilesAntisurface()
    try:
        arme.fire_at(50, 50, 10)
    except OutOfRangeError as e:
        assert str(e) == "Target is out of range"

def test_arma_lance_torpilles_munitions_epuisees():
    arme = LanceTorpilles()
    arme.munitions = 0
    try:
        arme.fire_at(0, 0, -10)
    except NoAmmunitionError as e:
        assert str(e) == "No ammunition left"

# Exécution des tests unitaires
test_arma_lance_missiles_antisurface()
test_arma_lance_missiles_antiair()
test_arma_lance_torpilles()
test_arma_lance_missiles_antisurface_hors_de_portee()
test_arma_lance_torpilles_munitions_epuisees()
