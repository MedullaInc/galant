'use strict';

describe('Gallant utility script', function () {
    describe('format function', function() {
        it('substitutes strings for {}', function () {
            expect('{0}, {1}'.format('a', 'b')).toEqual('a, b');
        });
    });

    describe('gallant.humanize function', function() {
        it('changes underscores to uppercase', function () {
            expect(window.gallant.humanize('hello_world')).toEqual('Hello World');
        });
    });

    describe('gallant.copyElement function', function() {
        it('copies element val() into destination, based on selector', function () {
            var source = jQuery('<div><input class="testclass" type="text" value="foobar"></div>');
            var dest = jQuery('<div><input class="testclass" type="text"></div>');

            expect(source.children(':first').val()).toEqual('foobar');

            window.gallant.copyElement(dest, source, '.testclass');
            expect(dest.children(':first').val()).toEqual(source.children(':first').val());
        });
    });
});