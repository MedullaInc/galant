'use strict';

describe('Gallant utility script', function () {
    it('adds format() function to String', function () {
        expect('foo'.format).toBeDefined();
    });
});